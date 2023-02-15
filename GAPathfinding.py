# ACHIEVEMENT: TODO: I got the AI to solve easy.png in 28 steps, 5 bumps and 1 dead end.
#	I don't remember the generation.
# 	The progress flat-zoned after a while. Probably due to several moves that should be REMOVED, and not REPLACED.
# 	Giving the mutations the ability to remove some random moves seems like a good idea.

# TODO: Optimization. Once a surviving creature has already ran, it doesn't need to run again.
#	It can simply idle.
# TODO: Mutating only the #1 creature may be detrimental to the algorithm's efficiency.
# TODO: The code, and my understanding of the code, are flawed.
#	I am not sure what is the X axis and what is the Y axis in all contexts.
# 	For example, the curr_pos appears to be "flipped" in respect to the XY grid.
# 	But, it is correct in respect to the maze ARRAY.
# TODO: hard.png makes all creatures die by the first laser. Why?
# TODO: Make the red tiles optional. Creatures should get an unedited maze as input.

from PIL import Image
import random
import tkinter
import os
from copy import deepcopy

import GAMazeGenerator
import GAHelper as Helper
from GAHelper import print_if_debug


GENERATION_AMOUNT_UNTIL_PAUSE = 250

INITIAL_MOVE_AMOUNT = 1500
MOVE_DOWN = 0
MOVE_LEFT = 1
MOVE_RIGHT = 2
MOVE_UP = 3

PENALTY_BUMP_INTO_WALL = 5
PENALTY_DEAD_END = 10
DEATH_BY_LASER_FITNESS = -99999
LENGTH_REWARD_PER_X = 250


def generate_random_color_rgb():
	rand_r = random.randrange(256)
	rand_g = random.randrange(256)
	rand_b = random.randrange(256)
	return (rand_r, rand_g, rand_b)


# The array is an array of <creature>'s, with the property <fitness>.
def insertion_sort_fitness(creature_arr):
	for second_creature_no in range(1, len(creature_arr)):
		current_creature = creature_arr[second_creature_no]
		i = second_creature_no - 1
		while i >= 0 and creature_arr[i].fitness < current_creature.fitness:
			creature_arr[i + 1] = creature_arr[i]
			i -= 1
		creature_arr[i + 1] = current_creature
	return creature_arr


class Creature:
	def __init__(self, p_generation, p_number, p_moves, p_parent=None):
		self.number = p_number
		self.generation = p_generation
		self.moves = p_moves
		self.parent = p_parent
		
		self.fitness = 0
		self.color = generate_random_color_rgb()
		self.finish_pos = None
		self.penalty_counters = None

	def __str__(self):
		if self.fitness == 0:  # 0 is impossible for a creature to achieve.
			return "Creature #{0} of generation {1} (Unknown fitness)".format(str(self.number), str(self.generation))
		if self.success:
			return "Creature #{0} of generation {1} (PASSED the maze, with the fitness of {2})"\
				.format(str(self.number), str(self.generation), Helper.OK_BLUE + str(self.fitness) + Helper.END_C)
		return "Creature #{0} of generation {1} (It failed the maze, with the fitness of {2})"\
			.format(str(self.number), str(self.generation), str(self.fitness))

	def __repr__(self):
		return "Creature(generation = {0}, number = {1}, move_amount = {2}, fitness = {3})".format(str(self.generation), str(self.number), str(len(self.moves)), str(self.fitness))

	def get_fitness_status(self):
		if self.fitness == 0:
			return "This is creature #{0} of generation {1}.\nIts fitness is unknown yet.".format(str(self.number), str(self.generation))
		if not self.success:
			return "This is creature #{0} of generation {1}.\nIt failed the maze, with the fitness of {2}."\
				.format(str(self.number), str(self.generation), str(self.fitness))
		return "This is creature #{0} of generation {1}.\nIt PASSED the maze, with the fitness of {2}."\
			.format(str(self.number), str(self.generation), Helper.OK_BLUE + str(self.fitness) + Helper.END_C)

	def get_finish_status(self):
		if self.finish_pos is None:
			return "Its finish pos is undefined."
		else:
			return "Its finish pos is: " + str(self.finish_pos) + ". Moves: " + str(len(self.moves)) + ". Penalties: " + str(self.penalty_counters)

	def get_generation(self):
		return self.generation

	def get_fitness(self):
		return self.fitness

	def get_moves(self):
		return self.moves

	def get_moves_concentrated_string(self):
		string = ""
		for move in self.moves:
			string += str(move)
		return string

	def get_number(self):
		return self.number

	def get_parent(self):
		return self.parent

	def get_success(self):
		return self.success

	def set_generation(self, p_generation):
		self.generation = p_generation

	def set_number(self, p_number):
		self.number = p_number

	def set_fitness(self, p_fitness):
		self.fitness = p_fitness

	def set_moves(self, p_moves):
		self.moves = p_moves

	def set_parent(self, p_parent):
		self.parent = p_parent
	
	# Currently causes the first creature's fitness to be scrambled, for unknown reasons.
	#
	# Differences from the start to the end of the method:
	# 	Same: moves, maze (all: start & end pos + arr2d)
	# 	Different: fitness, bump/dead-end amounts
	def solve_maze(self, maze):
		"""Solves the maze <maze_2d_array>, with the size of <size_x> by <size_y>, and puts amount of moves needed to solve inside <self.fitness>"""
		curr_pos = maze.get_start_pos()
		end_pos = maze.get_end_pos()
		move_no = 0
		self.fitness = 0
		self.success = False
		valid_maze_tiles = [Helper.COLOR_WHITE, Helper.COLOR_GREEN, Helper.COLOR_BLUE, Helper.COLOR_RED]
		#print_if_debug("My initial move list is:\n" + str(self.moves))
		maze_arr = maze.get_array2d()
		
		self.penalty_counters = {"bump": 0, "deadend": 0}
		death_laser_amount = 0
		death_laser_times = [20, len(self.moves) * 0.2, len(self.moves) * 0.45, len(self.moves) * 0.7]
		death_laser_x_targets = [Helper.maze_size_x * 0.05, Helper.maze_size_x * 0.15, Helper.maze_size_x * 0.3, Helper.maze_size_x * 0.5]
		
		# Perhaps "curr_pos != end_pos" doesn't work?
		while curr_pos != end_pos and move_no != len(self.moves):
			self.fitness -= 1  # <self.fitness> starts with 0, then decreases gradually
			if self.moves[move_no] == MOVE_DOWN:
				if curr_pos[0] != len(maze_arr) - 1:  # If the <curr_pos> is not on the bottom border
					if maze_arr[curr_pos[0] + 1][curr_pos[1]] in valid_maze_tiles:  # If the position below <curr_pos> is a part of the maze
						curr_pos = (curr_pos[0] + 1, curr_pos[1])
						if maze_arr[curr_pos[0] + 1][curr_pos[1]] == Helper.COLOR_RED:
							self.fitness -= PENALTY_DEAD_END
							self.penalty_counters["deadend"] += 1
					else:
						self.fitness -= PENALTY_BUMP_INTO_WALL
						self.penalty_counters["bump"] += 1
				else:
					self.fitness -= PENALTY_BUMP_INTO_WALL
					self.penalty_counters["bump"] += 1
			elif self.moves[move_no] == MOVE_LEFT:
				if curr_pos[1] != 0:  # If the <curr_pos> is not on the bottom border
					if maze_arr[curr_pos[0]][curr_pos[1] - 1] in valid_maze_tiles:  # If the position below <curr_pos> is a part of the maze
						curr_pos = (curr_pos[0], curr_pos[1] - 1)
						if maze_arr[curr_pos[0] + 1][curr_pos[1]] == Helper.COLOR_RED:
							self.fitness -= PENALTY_DEAD_END
							self.penalty_counters["deadend"] += 1
					else:
						self.fitness -= PENALTY_BUMP_INTO_WALL
						self.penalty_counters["bump"] += 1
				else:
					self.fitness -= PENALTY_BUMP_INTO_WALL
					self.penalty_counters["bump"] += 1
			elif self.moves[move_no] == MOVE_RIGHT:
				if curr_pos[1] != len(maze_arr[0]) - 1:  # If the <curr_pos> is not on the bottom border
					if maze_arr[curr_pos[0]][curr_pos[1] + 1] in valid_maze_tiles:  # If the position below <curr_pos> is a part of the maze
						curr_pos = (curr_pos[0], curr_pos[1] + 1)
						if maze_arr[curr_pos[0] + 1][curr_pos[1]] == Helper.COLOR_RED:
							self.fitness -= PENALTY_DEAD_END
							self.penalty_counters["deadend"] += 1
					else:
						self.fitness -= PENALTY_BUMP_INTO_WALL
						self.penalty_counters["bump"] += 1
				else:
					self.fitness -= PENALTY_BUMP_INTO_WALL
					self.penalty_counters["bump"] += 1
			elif self.moves[move_no] == MOVE_UP:
				if curr_pos[0] != 0:  # If the <curr_pos> is not on the top border
					if maze_arr[curr_pos[0] - 1][curr_pos[1]] in valid_maze_tiles:  # If the position below <curr_pos> is a part of the maze
						curr_pos = (curr_pos[0] - 1, curr_pos[1])
						if maze_arr[curr_pos[0] + 1][curr_pos[1]] == Helper.COLOR_RED:
							self.fitness -= PENALTY_DEAD_END
							self.penalty_counters["deadend"] += 1
					else:
						self.fitness -= PENALTY_BUMP_INTO_WALL
						self.penalty_counters["bump"] += 1
				else:
					self.fitness -= PENALTY_BUMP_INTO_WALL
					self.penalty_counters["bump"] += 1
			else:
				raise Exception("Unexpected move in solve_maze")
			move_no += 1
			
			# Only the current death laser
			if move_no > death_laser_times[death_laser_amount]:
				if curr_pos[death_laser_amount] < death_laser_x_targets[death_laser_amount]:
					self.fitness = DEATH_BY_LASER_FITNESS + death_laser_amount
					death_laser_amount += 1
					print_if_debug("Death by laser #{0}: ".format(death_laser_amount), curr_pos, death_laser_x_targets[death_laser_amount])
					return
			
#			# All death lasers
#			for laser_no in range(len(death_laser_x_targets)):
#				if death_laser_amount == laser_no and move_no > death_laser_times[laser_no]:
#					if curr_pos[laser_no] < death_laser_x_targets[laser_no]:
#						self.fitness = DEATH_BY_LASER_FITNESS
#						death_laser_amount += 1
#						print("Death by laser #{0}: ".format(laser_no), curr_pos, death_laser_x_targets[laser_no])
#						return

		if move_no != len(self.moves):
			self.moves = self.moves[:move_no]
			print_if_debug("Success! Fitness = {0}, Needed move amount = {1}".format(str(self.fitness), str(len(self.moves))))
			self.success = True
		
		self.finish_pos = curr_pos
		x_axis_steps = curr_pos[1]
		self.fitness += LENGTH_REWARD_PER_X * x_axis_steps
		#print(str(self.number) + "-" + str(self.generation) + ", " + str(self.finish_pos))
		#print(str(self.number) + "-" + str(self.generation) + ", " + str(penalty_counters))
	
	# TODO: This method might not be very efficient at improving the creatures, I'd say.
	def generate_mutated_moves(self):
		# ASSUMPTION: there are AT LEAST 120 moves (a roughly "good" amount)
		self.set_fitness(0)

		old_moves = []
		for move in self.moves:
			old_moves.append(move)
		
		move_amount = len(self.moves)
		
		# TODO: Replace the loop with: For all moves, 1% to change
		# TODO (SUGGESTION): If close to end, percentage raises from 1% up!
#		for move_no in range(int(move_amount*0.8), move_amount):
#			self.moves[move_no] = random.randrange(4)
			
#		for move_no in range(0, move_amount):
#			if random.randrange(10) == 1:  # 10% for move mutation!
#				self.moves[move_no] = random.randrange(4)
		
		for move_no in range(0, move_amount):
			# 5%, ?, ..., 50%
			# 0, 1, 2, ..., len
			# nth move? ()% of move mutation!
			mutation_chance = 0.05 + 0.45 * (move_no) / move_amount
			if random.random() <= mutation_chance:
				self.moves[move_no] = random.randrange(4)

		return old_moves
	
	def mutate(self):
		this.set_moves(this.generate_mutated_moves())
	
	def copy_other(self, other):
		self.set_generation(other.get_generation())
		self.set_number(other.get_number())
		self.set_moves(deepcopy(other.get_moves()))
		self.set_parent(other.get_parent())
		self.set_fitness(other.get_fitness())


def turn_1d_array_to_2d_arrayf(array, size_x, size_y):
	"""The function turns a 1d array (<array>) to a 2d array with the size of <size_x> by <size_y>"""
	maze_2d_array = []
	for x in range(size_x):
		maze_2d_array.append([])
		for y in range(size_y):
			maze_2d_array[x].append(array[x*size_x + y])
	return maze_2d_array


def get_maze_2d_array():
	file_name = input("Choose the maze image file: ")
	original_img1 = Image.open(Helper.maze_save_path + file_name + ".png")
	maze_1d_array = list(original_img1.getdata())
	(Helper.maze_size_x, Helper.maze_size_y) = original_img1.size
	return turn_1d_array_to_2d_arrayf(maze_1d_array, Helper.maze_size_x, Helper.maze_size_y)


def generate_creatures(generation, creature_amount, mutation_inheritor):
	# <mutation_inheritor> has the best creature, from which new creatures will inherit some moves.
	# For now, there is only one creature to mutate from.
	allowed_move_amount = INITIAL_MOVE_AMOUNT
	creatures = []
	if mutation_inheritor is not None:  # Used in all the generations, which are not generation #1, which all have 50 creatures
		mutation_inheritor_copy = Creature(0, 0, [])
		mutation_inheritor_copy.copy_other(mutation_inheritor)
		mutation_inheritor_copy.set_generation(generation)
		mutation_inheritor_copy.set_number(1)
		mutation_inheritor_copy.set_fitness(0)
		mutation_inheritor_copy.set_parent(mutation_inheritor)
		
		# All of the creatures will be mutated.
		for x in range(creature_amount):
			moves = mutation_inheritor_copy.generate_mutated_moves()
			creatures.append(Creature(generation, x + 1, moves, mutation_inheritor))
	else:
		# ASSUMPTION This is the first generation, which has 100 creatures
		for x in range(creature_amount):
			moves = []
			for y in range(allowed_move_amount):
				moves.append(random.randrange(4))  # 0 = down, 1 = left, 2 = right, 3 = up
			creatures.append(Creature(generation, x + 1, moves))  # Creature's info = Number, list of <allowed_move_amount> random numbers
	
	#print_if_debug("Generated new creatures: ", creatures)
	return creatures


# Currently, amount is meant to be half of the current population. Half of len(creatures)?
def kill_and_replace_creatures(creatures, generation, amount):
	"""The function replaces the worst 50% creatures with new creatures"""
	# http://www.geeksforgeeks.org/insertion-sort/
	new_100_creatures = insertion_sort_fitness(creatures)
	new_100_creatures = new_100_creatures[:int(amount)]  # Cuts in half

	if new_100_creatures[0].fitness >= -10000:  # Didn't die a horrible death.
		#print("[!!!!!] Previous ruler LIVED.")
		new_50_gen_creatures = generate_creatures(generation, amount, new_100_creatures[0])  # <amount> will probably always be 50, but who knows?
	else:
		#print("[!!!!!] Previous ruler died a horrible death.")
		new_50_gen_creatures = generate_creatures(generation, amount, None)

	for creature_no in range(len(new_50_gen_creatures)):
		new_100_creatures.append(new_50_gen_creatures[creature_no])

	return new_100_creatures


def print_creatures(creatures):
	passed_amount = 0
	top_fitness = -9999
	top_fitness_creature = None
	for creature_no in range(len(creatures)):
		creature = creatures[creature_no]
		if creature.get_success():
			passed_amount += 1
		if creature.fitness > top_fitness:
			top_fitness = creature.fitness
			top_fitness_creature = creature
		print(str(creature_no + 1) + ") " + str(creature))
		print(creature.get_finish_status())
		print("Parent: " + repr(creature.get_parent()))
		print_if_debug(creature.get_moves_concentrated_string()[:50] + "...")
		print()
	print("The amount of successful creatures is: " + str(passed_amount))
	print("The best creature: " + str(top_fitness_creature))
	if top_fitness_creature is not None:
		print(top_fitness_creature.get_finish_status())
	#print_if_debug("Showing creature #1:")
	# # # display_movement(creatures[0], )


# unused? (TODO)
# def display_movement(creature, maze):
# 	for i in range(len(creature.get_moves())):
# 		display_arr = creature_move_in_array(creature, i, maze)
#
# 		# display_1d_arrayf(img, )


# unused? (TODO)
# def creature_move_in_array(creature, move_count, maze):
# 	# maze = 2d array
# 	img = Image.new("RGB", (len(maze), len(maze[0])))
# 	# maze_1d_array = Helper.turn_2d_array_to_1d_arrayf(maze) unused? (TODO)
#
# 	curr_pos = maze.get_start_pos()
# 	move_no = 0
# 	size_x = len(maze)
# 	size_y = len(maze[0])
# 	while curr_pos != maze.get_end_pos() and move_no != len(creature.moves):
# 		if creature.moves[move_no] == 0:  # If the chosen move is down
# 			if curr_pos[0] != size_x - 1:  # If the <curr_pos> is not on the bottom border
# 				if maze[curr_pos[0] + 1][curr_pos[1]] == Helper.COLOR_WHITE:  # If the position bellow <curr_pos> is a part of the maze
# 					curr_pos = (curr_pos[0] + 1, curr_pos[1])
# 		elif creature.moves[move_no] == 1:  # If the chosen move is left
# 			if curr_pos[1] != 0:  # If the <curr_pos> is not on the bottom border
# 				if maze[curr_pos[0]][curr_pos[1] - 1] == Helper.COLOR_WHITE:  # If the position bellow <curr_pos> is a part of the maze
# 					curr_pos = (curr_pos[0], curr_pos[1] - 1)
# 		elif creature.moves[move_no] == 2:  # If the chosen move is right
# 			if curr_pos[1] != size_y - 1:  # If the <curr_pos> is not on the bottom border
# 				if maze[curr_pos[0]][curr_pos[1] + 1] == Helper.COLOR_WHITE:  # If the position bellow <curr_pos> is a part of the maze
# 					curr_pos = (curr_pos[0], curr_pos[1] + 1)
# 		elif creature.moves[move_no] == 3:  # If the chosen move is up
# 			if curr_pos[0] != 0:  # If the <curr_pos> is not on the top border
# 				if maze[curr_pos[0] - 1][curr_pos[1]] == Helper.COLOR_WHITE:  # If the position bellow <curr_pos> is a part of the maze
# 					curr_pos = (curr_pos[0] - 1, curr_pos[1])
# 		else:
# 			raise Exception("Unexpected move in creature_move_in_array")
# 		move_no += 1
#
# 	Helper.display_imgf(img, )
# 	return img


def solve_creatures(creatures, maze):
	for creature in creatures:
		#print_if_debug("Before:" + repr(creature))
		creature.solve_maze(maze)
		#print_if_debug("After:" + repr(creature))
	return creatures


def main():
	print("Warning: After exiting this script, the AI will reset.")
	
	maze_2d_array = get_maze_2d_array()
	start_pos, end_pos = 0, 0  # Both's values will change.
	for x in range(Helper.maze_size_x):
		if maze_2d_array[x][0] == Helper.COLOR_GREEN:
			start_pos = (x, 0)
			print_if_debug("Found start_pos!")
		if maze_2d_array[x][Helper.maze_size_y - 1] == Helper.COLOR_BLUE:
			end_pos = (x, Helper.maze_size_y - 1)
			print_if_debug("Found end_pos!")

	maze = Helper.Maze(maze_2d_array, start_pos, end_pos)
	
	print()
	print("When generating creatures, every {0} generations, you will be given the option to stop,".format(GENERATION_AMOUNT_UNTIL_PAUSE))
	print("    or to continue running the AI, allowing the population to get better.")
	print('This "breed" of creatures is not smart:')
	print("When they fail, they will often not improve, due to a overly simplistic Genetic algorithm.")
	print('The creatures will also much more often FAIL more complex mazes.')
	print('    I suggest using an easy maze for this simple algorithm to work.')
	print()
	print('The fitness of a creature defines how "badly" it did.')
	print('If a creature got to the end after 1400 steps, its fitness will be -1400.')
	print('If a creature bumped into a wall, got to a dead end, or was too slow - penalty.')
	print("The creatures' goal is to get their fitness as close to 0 as possible.")
	print()
	input("To generate creatures, enter anything.")
	
	print("Generating...")
	print()
	generation = 1
	creatures = generate_creatures(generation, 100, None)
	creatures = solve_creatures(creatures, maze)
	if Helper.is_debug:
			print_creatures(creatures)
			input("Next?")

	answer = ""
	while answer == "":
		generation += 1
		creatures = kill_and_replace_creatures(creatures, generation, 50)
		
		creatures = solve_creatures(creatures, maze)
		
		print_if_debug("AFTER: ", creatures)
		
		if generation % 25 == 0:
			print("Passed {0} generations!".format(generation))
		if generation % GENERATION_AMOUNT_UNTIL_PAUSE == 0:
			print()
			print_creatures(creatures)
			answer = input("To generate creatures, enter nothing. Else, enter anything that isn't blank.\n")
		elif Helper.is_debug:
			print_creatures(creatures)
			input("Next?")


if __name__ == "__main__":
	main()
