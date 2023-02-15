# TODO: Make the red tiles optional. Creatures should get an unedited maze as input.

from PIL import Image
import random
import GAHelper as Helper
from GAHelper import Maze
from copy import deepcopy
import math


def move_down(maze, curr_pos):
	"""The function moves the maze (<maze_2d_array>), with the size of size_x by size_y, creator's position down"""
	arr = maze.get_array2d()

	if curr_pos[1] == 1:  # On the top boundary
		new_pos = curr_pos
	else:  # Anywhere in the middle/on the bottom border
		new_pos = (curr_pos[0], curr_pos[1] - 1)
		possible_flag = False
		if arr[new_pos[0]][new_pos[1] - 1] == Helper.COLOR_BLACK:
			# current = O, black = █ (alt+219), new = V, checked = 1, 2, 3...
			# 415
			# 3^2
			# █O█
			if arr[new_pos[0] + 1][new_pos[1]] == Helper.COLOR_BLACK:
				if arr[new_pos[0] - 1][new_pos[1]] == Helper.COLOR_BLACK:
					if arr[new_pos[0] - 1][new_pos[1] - 1] == Helper.COLOR_BLACK:
						if arr[new_pos[0] + 1][new_pos[1] - 1] == Helper.COLOR_BLACK:
							if arr[new_pos[0]][new_pos[1]] != Helper.COLOR_WHITE:
								arr[new_pos[0]][new_pos[1]] = Helper.COLOR_WHITE
								possible_flag = True
		if not possible_flag:
			new_pos = curr_pos

	return new_pos


def move_left(maze, curr_pos):
	"""The function moves the maze (<maze_2d_array>), with the size of size_x by size_y, creator's position left"""
	arr = maze.get_array2d()
	if curr_pos[0] == 1:  # On the left boundary
		new_pos = curr_pos
	elif curr_pos[1] == 1:  # On the top boundary
		possible_flag = False
		new_pos = (curr_pos[0] - 1, curr_pos[1])
		# current = O, black = █ (alt+219), new = <, checked = 1, 2, 3..., border = -
		# ---
		# 1<O
		# 32█
		if arr[new_pos[0] - 1][new_pos[1]] == Helper.COLOR_BLACK:
			if arr[new_pos[0]][new_pos[1] + 1] == Helper.COLOR_BLACK:
				if arr[new_pos[0] - 1][new_pos[1] + 1] == Helper.COLOR_BLACK:
					if arr[new_pos[0]][new_pos[1]] != Helper.COLOR_WHITE:
						arr[new_pos[0]][new_pos[1]] = Helper.COLOR_WHITE
						possible_flag = True
		if not possible_flag:
			new_pos = curr_pos
	elif curr_pos[1] == len(arr) - 2:  # On the bottom boundary
		possible_flag = False
		new_pos = (curr_pos[0], curr_pos[1] - 1)
		# current = O, black = █ (alt+219), new = <, checked = 1, 2, 3..., border = -
		# 32█
		# 1<O
		# ---
		if arr[new_pos[0] - 1][new_pos[1]] == Helper.COLOR_BLACK:
			if arr[new_pos[0]][new_pos[1] - 1] == Helper.COLOR_BLACK:
				if arr[new_pos[0] - 1][new_pos[1] - 1] == Helper.COLOR_BLACK:
					if arr[new_pos[0]][new_pos[1]] != Helper.COLOR_WHITE:
						arr[new_pos[0]][new_pos[1]] = Helper.COLOR_WHITE
						possible_flag = True
		if not possible_flag:
			new_pos = curr_pos
	else:  # Anywhere in the middle
		new_pos = (curr_pos[0] - 1, curr_pos[1])
		possible_flag = False
		if arr[new_pos[0] - 1][new_pos[1]] == Helper.COLOR_BLACK:
			# current = O, black = █ (alt+219), new = <, checked = 1, 2, 3...
			# 43█
			# 1<O
			# 52█
			if arr[new_pos[0]][new_pos[1] + 1] == Helper.COLOR_BLACK:
				if arr[new_pos[0]][new_pos[1] - 1] == Helper.COLOR_BLACK:
					if arr[new_pos[0] - 1][new_pos[1] - 1] == Helper.COLOR_BLACK:
						if arr[new_pos[0] - 1][new_pos[1] + 1] == Helper.COLOR_BLACK:
							if arr[new_pos[0]][new_pos[1]] != Helper.COLOR_WHITE:
								arr[new_pos[0]][new_pos[1]] = Helper.COLOR_WHITE
								possible_flag = True
		if not possible_flag:
			new_pos = curr_pos
	return new_pos


def move_right(maze, curr_pos):
	"""The function moves the maze (<maze_2d_array>), with the size of size_x by size_y, creator's position right"""
	arr = maze.get_array2d()

	if curr_pos[0] == Helper.maze_size_x - 2:
		# MADE IT!
		new_pos = (curr_pos[0] + 1, curr_pos[1])
		arr[new_pos[0]][new_pos[1]] = Helper.COLOR_WHITE
	elif curr_pos[1] == 1:  # On the top boundary
		new_pos = (curr_pos[0] + 1, curr_pos[1])
		possible_flag = False
		# current = O, black = █ (alt+219), new = >, checked = 1, 2, 3..., border = -
		# ---
		# O>1
		# █23
		if arr[new_pos[0] + 1][new_pos[1]] == Helper.COLOR_BLACK:
			if arr[new_pos[0]][new_pos[1] + 1] == Helper.COLOR_BLACK:
				if arr[new_pos[0] + 1][new_pos[1] + 1] == Helper.COLOR_BLACK:
					if arr[new_pos[0]][new_pos[1]] != Helper.COLOR_WHITE:
						arr[new_pos[0]][new_pos[1]] = Helper.COLOR_WHITE
						possible_flag = True
		if not possible_flag:
			new_pos = curr_pos
	elif curr_pos[1] == Helper.maze_size_y - 2:  # On the bottom boundary
		new_pos = (curr_pos[0] + 1, curr_pos[1])
		possible_flag = False
		# current = O, black = █ (alt+219), new = >, checked = 1, 2, 3..., border = -
		# █23
		# O>1
		# ---
		if arr[new_pos[0] + 1][new_pos[1]] == Helper.COLOR_BLACK:
			if arr[new_pos[0]][new_pos[1] - 1] == Helper.COLOR_BLACK:
				if arr[new_pos[0] + 1][new_pos[1] - 1] == Helper.COLOR_BLACK:
					if arr[new_pos[0]][new_pos[1]] != Helper.COLOR_WHITE:
						arr[new_pos[0]][new_pos[1]] = Helper.COLOR_WHITE
						possible_flag = True
		if not possible_flag:
			new_pos = curr_pos
	else:  # Not on the boundaries
		if curr_pos[0] == 0:  # The start position
			new_pos = (curr_pos[0] + 1, curr_pos[1])
			arr[new_pos[0]][new_pos[1]] = Helper.COLOR_WHITE
		else:  # Anywhere in the middle
			new_pos = (curr_pos[0] + 1, curr_pos[1])
			possible_flag = False
			# print("...", new_pos)
			# Helper.display_2d_arrayf(maze.get_array2d(), Helper.display_ratio, 5)
			if arr[new_pos[0] + 1][new_pos[1]] == Helper.COLOR_BLACK:
				# current = O, black = █ (alt+219), new = >, checked = 1, 2, 3...
				# █34
				# O>1
				# █25
				if arr[new_pos[0]][new_pos[1] + 1] == Helper.COLOR_BLACK:
					if arr[new_pos[0]][new_pos[1] - 1] == Helper.COLOR_BLACK:
						if arr[new_pos[0] + 1][new_pos[1] - 1] == Helper.COLOR_BLACK:
							if arr[new_pos[0] + 1][new_pos[1] + 1] == Helper.COLOR_BLACK:
								if arr[new_pos[0]][new_pos[1]] != Helper.COLOR_WHITE:
									arr[new_pos[0]][new_pos[1]] = Helper.COLOR_WHITE
									possible_flag = True
			if not possible_flag:
				new_pos = curr_pos
	# Helper.display_2d_arrayf(maze.get_array2d(), Helper.display_ratio, 0.1)
	return new_pos


def move_up(maze, curr_pos):
	"""The function moves the maze (<maze_2d_array>), with the size of size_x by size_y, creator's position up"""
	arr = maze.get_array2d()
	# print(curr_pos)
	if curr_pos[1] == Helper.maze_size_y - 2:  # On the bottom boundary
		new_pos = (curr_pos[0], curr_pos[1])
	else:  # Anywhere in the middle/  # On the top boundary
		new_pos = (curr_pos[0], curr_pos[1] + 1)
		possible_flag = False
		if arr[new_pos[0]][new_pos[1] + 1] == Helper.COLOR_BLACK:
			# current = O, black = █ (alt+219), new = V, checked = 1, 2, 3...
			# █O█
			# 3V2
			# 415
			if arr[new_pos[0] + 1][new_pos[1]] == Helper.COLOR_BLACK:
				if arr[new_pos[0] - 1][new_pos[1]] == Helper.COLOR_BLACK:
					if arr[new_pos[0] - 1][new_pos[1] + 1] == Helper.COLOR_BLACK:
						if arr[new_pos[0] + 1][new_pos[1] + 1] == Helper.COLOR_BLACK:
							if arr[new_pos[0]][new_pos[1]] != Helper.COLOR_WHITE:
								# █O█
								# █V█
								# ███
								arr[new_pos[0]][new_pos[1]] = Helper.COLOR_WHITE
								possible_flag = True

		if not possible_flag:
			new_pos = curr_pos

	return new_pos


def get_to_endf(maze, curr_pos, get_to_end):
	"""The function forwards the current position (<curr_pos>) to the end position randomly, at a maze (<maze>)"""
	# test_maze = deepcopy(maze)
	arr = maze.get_array2d()
	main_path_stuck = False

	if curr_pos == maze.get_start_pos():
		curr_pos = move_right(maze, curr_pos)
	nothing_happened_counter = 0
	allowed_nothing_happened_moments = 20
	# Helper.display_2d_arrayf(maze.get_array2d(), Helper.display_ratio, 3)
	if get_to_end:
		# main path
		while curr_pos[0] != Helper.maze_size_x - 1 and nothing_happened_counter < allowed_nothing_happened_moments:
			# This line V decides what is the sequence of if's will be
			random_num = random.randrange(4)
			# print("1. ", curr_pos)
			if random_num == 0:
				# print("DOWN (▲)")
				new_pos = move_down(maze, curr_pos)
			elif random_num == 1:
				# print("LEFT")
				new_pos = move_left(maze, curr_pos)
			elif random_num == 2:
				# print("RIGHT")
				new_pos = move_right(maze, curr_pos)
			elif random_num == 3:
				# print("UP (▼)")
				new_pos = move_up(maze, curr_pos)
			else:
				raise Exception("Wrong random number")
			# Helper.display_2d_arrayf(maze.get_array2d(), Helper.display_ratio, 0.2)
			if new_pos == curr_pos:
				nothing_happened_counter += 1
			else:
				nothing_happened_counter = 0

			curr_pos = new_pos

		if nothing_happened_counter >= allowed_nothing_happened_moments:
			main_path_stuck = True
			maze.set_end_pos(curr_pos)
		else:
			maze.array2d[curr_pos[0]][curr_pos[1]] = Helper.COLOR_BLUE
	else:
		# random branch
		while curr_pos[0] < Helper.maze_size_x - 2 and nothing_happened_counter < allowed_nothing_happened_moments:
			# This line V decides what is the sequence of if's will be
			random_num = random.randrange(4)
			if random_num == 0:
				new_pos = move_down(maze, curr_pos)
			elif random_num == 1:
				new_pos = move_left(maze, curr_pos)
			elif random_num == 2:
				new_pos = move_right(maze, curr_pos)
			elif random_num == 3:
				new_pos = move_up(maze, curr_pos)
			else:
				raise Exception("Wrong random number")
			if 0 <= random_num <= 3:
				if new_pos == curr_pos:
					nothing_happened_counter += 1
				else:
					nothing_happened_counter = 0
				curr_pos = new_pos
	# print("Finished a random branch?")
	# Helper.display_2d_arrayf(arr, Helper.display_ratio, 0.2)

	# Helper.display_2d_arrayf(maze.get_array2d(), Helper.display_ratio, 3)

	# print(main_path_stuck)
	return maze, main_path_stuck


def random_mazef(size_x, size_y):
	"""The function creates a randomized maze with the size of <size_x> by <size_y>"""
	
	needed_path_white_amount = int(math.pow(1.08, (Helper.maze_size_x + Helper.maze_size_y) / 2) * 8.6)  # MAGIC FORMULA
	print("STEP 1: Generate a path from the maze's randomized start point to the other side.")
	print("Path pixels required: ", needed_path_white_amount)
	
	maze = Helper.Maze([], None, None)

	while True:
		for x in range(size_x):
			maze.array2d.append([])
			for y in range(size_y):
				maze.array2d[x].append(Helper.COLOR_BLACK)

		start_pos_random_y = random.randrange(1, size_y - 1)
		start_pos = (0, start_pos_random_y)
		maze.set_start_pos(start_pos)
		maze.array2d[maze.start_pos[0]][maze.start_pos[1]] = Helper.COLOR_GREEN

		temp_maze = deepcopy(maze)
		temp_maze, is_stuck_flag = get_to_endf(temp_maze, temp_maze.start_pos, True)
		while is_stuck_flag:
			temp_maze = deepcopy(maze)
			temp_maze, is_stuck_flag = get_to_endf(temp_maze, temp_maze.start_pos, True)
		maze = deepcopy(temp_maze)

		blue_found_flag = False
		for y in range(size_y):  # Checks in the last column for the blue slot (needed)
			if maze.get_array2d()[size_x - 1][y] == Helper.COLOR_BLUE:
				blue_found_flag = True
				break
		white_amount = 0
		for x in range(size_x):
			for y in range(size_y):
				if maze.get_array2d()[x][y] == Helper.COLOR_WHITE:
					white_amount += 1
		
		# Do-while loop emulation.
		if (not blue_found_flag) or (not (white_amount >= needed_path_white_amount)):
			break
		
		maze.array2d = []

	print("Finished generating the correct path! ({0} white cells)".format(str(white_amount)))
	print("Close the maze display to proceed.")
	Helper.display_2d_arrayf(maze.get_array2d(), Helper.display_ratio)
	
	needed_white_amount = int(math.pow(1.13, (Helper.maze_size_x + Helper.maze_size_y) / 2) * 7)  # MAGIC FORMULA
	print("STEP 2: Generate random sub-paths that branch out of the main path.")
	print("Remaining maze pixels required: ", needed_white_amount)
	
	while not white_amount >= needed_white_amount:
		white_amount = 0
		for x in range(1, size_x - 1):
			for y in range(size_y):
				random_num = random.randrange(4)  # 25% to spawn a path
				if maze.get_array2d()[x][y] == Helper.COLOR_WHITE and random_num % 4 == 0:
					get_to_endf(maze, (x, y), False)
					# print("New Branch!")
					# Helper.display_2d_arrayf(maze.get_array2d(), Helper.display_ratio, 3)
		for x in range(size_x):
			for y in range(size_y):
				if maze.get_array2d()[x][y] == Helper.COLOR_WHITE:
					white_amount += 1
	
	print("Finished adding random paths! ({0} white cells)".format(str(white_amount)))
	print("Close the maze display to proceed.")
	Helper.display_2d_arrayf(maze.get_array2d(), Helper.display_ratio)

	print("STEP 3: Randomly connecting the many pathes in the maze.")
	
	for x in range(1, size_x - 1):
		for y in range(1, size_y - 1):
			random_num = random.randrange(6)
			# current_checked = O, black = █ (alt+219), white = =, ? = doesn't matter
			# ?=?
			# █O█
			# ?=?
			if maze.get_array2d()[x][y] == Helper.COLOR_BLACK\
				and maze.get_array2d()[x][y - 1] == Helper.COLOR_BLACK\
				and maze.get_array2d()[x][y + 1] == Helper.COLOR_BLACK\
				and maze.get_array2d()[x - 1][y] == Helper.COLOR_WHITE\
				and maze.get_array2d()[x + 1][y] == Helper.COLOR_WHITE\
				and random_num % 8 == 0:
				maze.array2d[x][y] = Helper.COLOR_WHITE
				white_amount += 1

			# current_checked = O, black = █ (alt+219), white = ||, ? = doesn't matter
			# ?█?
			# ||O||
			# ?█?
			if maze.get_array2d()[x][y] == Helper.COLOR_BLACK\
				and maze.get_array2d()[x][y - 1] == Helper.COLOR_WHITE\
				and maze.get_array2d()[x][y + 1] == Helper.COLOR_WHITE\
				and maze.get_array2d()[x - 1][y] == Helper.COLOR_BLACK\
				and maze.get_array2d()[x + 1][y] == Helper.COLOR_BLACK\
				and random_num % 8 == 4:
				maze.array2d[x][y] = Helper.COLOR_WHITE
				white_amount += 1
	print("Finished connecting paths!".format(str(white_amount)))
	print("Close the maze display to proceed.")
	Helper.display_2d_arrayf(maze.get_array2d(), Helper.display_ratio)
	
	print("STEP 4: Colour the dead ends in red.")
	
	current_maze = deepcopy(maze.get_array2d())
	walkable_colours_without_red = [Helper.COLOR_WHITE, Helper.COLOR_GREEN, Helper.COLOR_BLUE, ]
	
	for x in range(1, size_x - 1):
		for y in range(1, size_y - 1):
			if current_maze[x][y] != Helper.COLOR_WHITE:
				continue
			white_neighbours = 0
			for point in [[x,y-1],[x,y+1],[x-1,y],[x+1,y],]:
				if current_maze[point[0]][point[1]] in walkable_colours_without_red:
					white_neighbours += 1
			if white_neighbours == 1:
				maze.array2d[x][y] = Helper.COLOR_RED
	
	return maze.get_array2d(), start_pos, maze.get_end_pos(), white_amount


def main():
	maze_2d_array, start_pos, end_pos, white_amount = random_mazef(Helper.maze_size_x, Helper.maze_size_y)
	print("Finished generating the maze! Total white cells: {0} white cells.".format(str(white_amount)))
	maze_1d_array2 = Helper.turn_2d_array_to_1d_arrayf(maze_2d_array)
	original_img1 = Image.new("RGB", (Helper.maze_size_x, Helper.maze_size_y))
	original_img1.putdata(maze_1d_array2)
	# Helper.display_1d_arrayf(maze_1d_array2, Helper.maze_size_x, Helper.maze_size_y, Helper.display_ratio, 0)

	print("Close the maze display to proceed. (Then, you will be offered to save the maze.)")
	Helper.display_2d_arrayf(maze_2d_array, Helper.display_ratio)
	
	print("Would you like to save the maze?\nYes - Write a file name\nNo - Press enter")
	file_name = input()
	if file_name != "":
		Helper.ensure_maze_save_path_exists()
		original_img1.save(Helper.maze_save_path + file_name + ".png")
		print("Maze saved!")
	else:
		print("Maze discarded!")

	print("Would you like to print the maze in ascii form?\nYes - Write anything\nNo - Press enter")
	want_ascii = input() != ""
	if want_ascii:
		print("Here's the maze, ascii-fied!:")
		maze = Maze(maze_2d_array, start_pos, end_pos)
		maze.print_asciified()
#		for j in range(len(maze_2d_array[0])):
#			for i in range(len(maze_2d_array)):
#				if maze_2d_array[i][j] == Helper.COLOR_BLACK:
#					maze_2d_array[i][j] = "▓"
#				if maze_2d_array[i][j] == Helper.COLOR_WHITE:
#					maze_2d_array[i][j] = "░"
#				if maze_2d_array[i][j] == Helper.COLOR_GREEN:
#					maze_2d_array[i][j] = "▒"
#				if maze_2d_array[i][j] == Helper.COLOR_BLUE:
#					maze_2d_array[i][j] = "▒"
#				print(maze_2d_array[i][j], end='')
#			print()


if __name__ == "__main__":
	main()
