from PIL import Image
import random
import tkinter
import os
import ga_maze_generator
import ga_helper as Helper


# color_black = (0, 0, 0)
# color_white = (255, 255, 255)
# color_red = (255, 255, 255)
# maze_size_x = 16
# maze_size_y = 16
# maze_size = (maze_size_x, maze_size_y)
# display_ratio = 8
# display_size = (maze_size_x*display_ratio, maze_size_y*display_ratio)
# temp_path = "C:\\Users\\magshimim\\Documents\\Art\\genetic\\temp2.png"
# maze_save_path = "C:\\Users\\magshimim\\Documents\\Art\\genetic\\mazes\\"
# OK_BLUE = '\033[94m'
# END_C = '\033[0m'


class Creature:
	def __init__(self, p_generation, p_number, p_moves):
		self.number = p_number
		self.moves = p_moves
		self.generation = p_generation
		self.fitness = 0
		rand_r = random.randrange(256)
		rand_g = random.randrange(256)
		rand_b = random.randrange(256)
		self.color = (rand_r, rand_g, rand_b)

	def __str__(self):
		if self.fitness == 0:
			return "This is creature #{0} of generation {1}.\nIts fitness is unknown yet.".format(str(self.number), str(self.generation))
		elif self.fitness == -1500:
			return "This is creature #{0} of generation {1}.\nIt failed the maze.".format(str(self.number), str(self.generation))
		else:
			return "This is creature #{0} of generation {1}.\nIt passed the maze, with the fitness of {2}."\
				.format(str(self.number), str(self.generation), Helper.OK_BLUE + str(self.fitness) + Helper.END_C)

	def __repr__(self):
		return "Creature(generation = {0}, number = {1}, move_amount = {2}, fitness = {3})".format(str(self.generation), str(self.number), str(len(self.moves)), str(self.fitness))

	def get_generation(self):
		return self.generation

	def get_fitness(self):
		return self.fitness

	def get_moves(self):
		return self.moves

	def get_number(self):
		return self.number

	def set_generation(self, p_generation):
		self.generation = p_generation

	def set_number(self, p_number):
		self.number = p_number

	def set_fitness(self, p_fitness):
		self.fitness = p_fitness

	def set_moves(self, p_moves):
		self.moves = p_moves

	def solve_maze(self, maze):
		"""Solves the maze <maze_2d_array>, with the size of <size_x> by <size_y>, and puts amount of moves needed to solve inside <self.fitness>"""
		curr_pos = maze.get_start_pos()
		move_no = 0
		self.fitness = 0
		# print("My moves are:\n" + str(self.moves))
		arr = maze.get_array2d()
		while curr_pos != maze.get_end_pos() and move_no != len(self.moves):
			self.fitness -= 1  # <self.fitness> starts with 0, then decreases gradually
			if self.moves[move_no] == 0:  # If the chosen move is down
				if curr_pos[0] != len(arr) - 1:  # If the <curr_pos> is not on the bottom border
					if arr[curr_pos[0] + 1][curr_pos[1]] == Helper.color_white:  # If the position bellow <curr_pos> is a part of the maze
						curr_pos = (curr_pos[0] + 1, curr_pos[1])
			elif self.moves[move_no] == 1:  # If the chosen move is left
				if curr_pos[1] != 0:  # If the <curr_pos> is not on the bottom border
					if arr[curr_pos[0]][curr_pos[1] - 1] == Helper.color_white:  # If the position bellow <curr_pos> is a part of the maze
						curr_pos = (curr_pos[0], curr_pos[1] - 1)
			elif self.moves[move_no] == 2:  # If the chosen move is right
				if curr_pos[1] != len(arr[0]) - 1:  # If the <curr_pos> is not on the bottom border
					if arr[curr_pos[0]][curr_pos[1] + 1] == Helper.color_white:  # If the position bellow <curr_pos> is a part of the maze
						curr_pos = (curr_pos[0], curr_pos[1] + 1)
			elif self.moves[move_no] == 3:  # If the chosen move is up
				if curr_pos[0] != 0:  # If the <curr_pos> is not on the top border
					if arr[curr_pos[0] - 1][curr_pos[1]] == Helper.color_white:  # If the position bellow <curr_pos> is a part of the maze
						curr_pos = (curr_pos[0] - 1, curr_pos[1])
			else:
				raise Exception("Unexpected move in solve_maze")
			move_no += 1

		if move_no != len(self.moves):
			self.moves = self.moves[:move_no]
			print("Success! Fitness = {0}, Needed move amount = {1}".format(str(self.fitness), str(len(self.moves))))

	def mutate(self):
		# assumed the move amount is 1500
		# assumed there are AT LEAST 120 moves
		self.set_fitness(0)

		old_moves = []
		for move in self.moves:
			old_moves.append(move)

		# TODO: Replace the loop with: For all moves, 1% to change
		# TODO (SUGGESTION): If close to end, percentage raises from 1% up!
		for move_no in range(int(len(self.moves)*0.8), len(self.moves)):
			self.moves[move_no] = random.randrange(4)

		return old_moves

	def copy_other(self, other):
		# new_creature.copy_other(old_creature)
		self.set_generation(other.get_generation())
		self.set_number(other.get_number())
		self.set_moves(other.get_moves())
		self.set_fitness(other.get_fitness())


# V Done!
def turn_1d_array_to_2d_arrayf(array, size_x, size_y):
	"""The function turns a 1d array (<array>) to a 2d array with the size of <size_x> by <size_y>"""
	maze_2d_array = []
	for x in range(size_x):
		maze_2d_array.append([])
		for y in range(size_y):
			maze_2d_array[x].append(array[x*size_x + y])
	return maze_2d_array


# V Done!
def get_maze_2d_array():
	file_name = input("Choose the maze image file: ")
	original_img1 = Image.open(Helper.maze_save_path + file_name + ".png")
	maze_1d_array = list(original_img1.getdata())
	return turn_1d_array_to_2d_arrayf(maze_1d_array, Helper.maze_size_x, Helper.maze_size_y)


# V Done!
def generate_creatures(generation, creature_amount, mutation_inheritor):
	# mutation_inheritor has the best result
	# for now, there is only one mutation
	allowed_move_amount = 1500
	creatures = []
	if mutation_inheritor is not None:  # Used in all the generations, which are not generation #1, which all have 50 creatures
		mutation_inheritor_copy = Creature(0, 0, [])
		mutation_inheritor_copy.copy_other(mutation_inheritor)
		mutation_inheritor_copy.set_generation(generation)
		mutation_inheritor_copy.set_number(1)
		mutation_inheritor_copy.set_fitness(0)
		old_moves = mutation_inheritor_copy.mutate()
		mutation_inheritor.set_moves(old_moves)
		# The first creature of each new generation is a mutation (except for generation #1)
		creatures.append(mutation_inheritor_copy)
		for x in range(1, creature_amount):
			moves = []
			for y in range(allowed_move_amount):
				moves.append(random.randrange(4))  # 0 = down, 1 = left, 2 = right, 3 = up
			creatures.append(Creature(generation, x + 1, moves))  # Creature's info = Number, list of <allowed_move_amount> random numbers
	else:  # Used in the first generation, which has 100 creatures
		for x in range(creature_amount):
			moves = []
			for y in range(allowed_move_amount):
				moves.append(random.randrange(4))  # 0 = down, 1 = left, 2 = right, 3 = up
			creatures.append(Creature(generation, x + 1, moves))  # Creature's info = Number, list of <allowed_move_amount> random numbers

	return creatures


# V Done!
def kill_and_replace_creatures(creatures, generation, amount):
	"""The function replaces the worst 50% creatures with new creatures"""
	# http://www.geeksforgeeks.org/insertion-sort/
	new_100_creatures = creatures

	for second_creature_no in range(1, len(new_100_creatures)):
		current_creature = new_100_creatures[second_creature_no]
		i = second_creature_no - 1
		while i >= 0 and new_100_creatures[i].fitness < current_creature.fitness:
			new_100_creatures[i + 1] = new_100_creatures[i]
			i = i - 1
		new_100_creatures[i + 1] = current_creature

	# By now, the creature list is sorted (by inserting)

	new_100_creatures = new_100_creatures[:int(amount)]  # Cuts in half

	if new_100_creatures[0].fitness != -1500:
		new_50_gen_creatures = generate_creatures(generation, amount, new_100_creatures[0])  # <amount> will probably always be 50, but who knows?
	else:
		new_50_gen_creatures = generate_creatures(generation, amount, None)

	for creature_no in range(len(new_50_gen_creatures)):
		new_100_creatures.append(new_50_gen_creatures[creature_no])

	# print("Fitness: " + str(new_100_creatures[0].get_fitness()))
	# print("moves: " + str(new_100_creatures[0].get_moves()))
	# print("Fitnesssss: " + str(new_100_creatures[50].get_fitness()))
	# print("movessssss: " + str(new_100_creatures[50].get_moves()))

	return new_100_creatures


# V Done!
def print_creatures(creatures):
	passed_amount = 0
	for creature_no in range(len(creatures)):
		if "passed" in str(creatures[creature_no]):
			passed_amount += 1
		print(str(creature_no + 1) + ") " + str(creatures[creature_no]))
		# print(creatures[creature_no].moves)
		print()
	print("The amount of passed creatures is: " + str(passed_amount))
	print("Showing creature #1:")
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
# 				if maze[curr_pos[0] + 1][curr_pos[1]] == Helper.color_white:  # If the position bellow <curr_pos> is a part of the maze
# 					curr_pos = (curr_pos[0] + 1, curr_pos[1])
# 		elif creature.moves[move_no] == 1:  # If the chosen move is left
# 			if curr_pos[1] != 0:  # If the <curr_pos> is not on the bottom border
# 				if maze[curr_pos[0]][curr_pos[1] - 1] == Helper.color_white:  # If the position bellow <curr_pos> is a part of the maze
# 					curr_pos = (curr_pos[0], curr_pos[1] - 1)
# 		elif creature.moves[move_no] == 2:  # If the chosen move is right
# 			if curr_pos[1] != size_y - 1:  # If the <curr_pos> is not on the bottom border
# 				if maze[curr_pos[0]][curr_pos[1] + 1] == Helper.color_white:  # If the position bellow <curr_pos> is a part of the maze
# 					curr_pos = (curr_pos[0], curr_pos[1] + 1)
# 		elif creature.moves[move_no] == 3:  # If the chosen move is up
# 			if curr_pos[0] != 0:  # If the <curr_pos> is not on the top border
# 				if maze[curr_pos[0] - 1][curr_pos[1]] == Helper.color_white:  # If the position bellow <curr_pos> is a part of the maze
# 					curr_pos = (curr_pos[0] - 1, curr_pos[1])
# 		else:
# 			raise Exception("Unexpected move in creature_move_in_array")
# 		move_no += 1
#
# 	Helper.display_imgf(img, )
# 	return img


# V DONE!
def solve_creatures(creatures, maze):
	for creature in creatures:
		# print("Before:" + repr(creature))
		creature.solve_maze(maze)
		# print("After:" + repr(creature))


def main():
	maze_2d_array = get_maze_2d_array()
	start_pos = 0  # This variable will 100% be changed
	end_pos = 0  # This variable will 100% be changed
	for x in range(Helper.maze_size_x):
		if maze_2d_array[x][0] == Helper.color_white:
			start_pos = (x, 0)
		if maze_2d_array[x][Helper.maze_size_y - 1] == Helper.color_white:
			end_pos = (x, Helper.maze_size_y - 1)

	maze = Helper.Maze(maze_2d_array, start_pos, end_pos)

	input("To generate creatures, enter anything.")
	generation = 1
	creatures = generate_creatures(generation, 100, None)
	solve_creatures(creatures, maze)
	print()
	answer = ""
	while answer == "":
		generation += 1
		creatures = kill_and_replace_creatures(creatures, generation, 50)
		# print("\n\nBEFORE SOLVE\n\n")
		# print_creatures(creatures)
		# solve_creatures(creatures, maze_2d_array, Helper.maze_size_x, Helper.maze_size_y, start_pos, end_pos)
		solve_creatures(creatures, maze_2d_array)
		# print("\n\nAFTER SOLVE\n\n")
		# print_creatures(creatures)
		if generation % 100 == 0:
			print("Passed 100 generations!")
		if generation % 1000 == 0:
			print()
			print_creatures(creatures)
			answer = input("To generate creatures, enter nothing. Enter anything that isn't blank, else.\n")


main()
