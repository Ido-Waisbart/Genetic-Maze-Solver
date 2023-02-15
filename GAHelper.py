from PIL import Image
import random
import tkinter
import os


is_debug = False


COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREEN = (0, 255, 0)  # start pos
COLOR_BLUE = (0, 0, 255)  # end pos
COLOR_RED = (255, 0, 0)  # dead end
maze_size_x = 32
maze_size_y = 32
maze_size = (maze_size_x, maze_size_y)
display_ratio = 8
display_size = (maze_size_x*display_ratio, maze_size_y*display_ratio)
dir_path = os.path.dirname(os.path.realpath(__file__))
temp_path = dir_path + r"\temp.png"
maze_save_path = dir_path + r"\mazes" + "\\"
OK_BLUE = ''
END_C = ''
#OK_BLUE = '\033[94m'  # Uncomment to activate, if supported.
#END_C = '\033[0m'  # Uncomment to activate, if supported.


def print_if_debug(*to_print):
	if is_debug:
		print(to_print)


def display_imgf(save_path, second_amount=0):
	"""The function displays an image, located at the path <save_path>,
		in a separate window for <second_amount> seconds."""
	root = tkinter.Tk("Image display!")
	second = 1000
	display_time = int(second_amount * second)
	label_display_img1 = tkinter.PhotoImage(file=save_path)
	#label_display_img1 = tkinter.PhotoImage(label_display_img1, Image.NEAREST)
	img_label = tkinter.Label(root, image=label_display_img1)
	img_label.label_display_img1 = label_display_img1
	img_label.pack()
	if second_amount != 0:
		root.after(display_time, lambda: root.destroy())
	root.configure(background='slategray1')
	root.lift()
	root.geometry('%dx%d+%d+%d' % (display_size[0], display_size[1], 0, 0))
	root.mainloop()


def turn_2d_array_to_1d_arrayf(array):
	"""The function turns a 2d array (array) to a 1d array"""
	maze_1darray = []
	for y in range(maze_size_y):
		for x in range(maze_size_x):
			maze_1darray.append(array[x][y])
	return maze_1darray


def display_2d_arrayf(arr, scale_ratio, seconds=0):
	"""The function displays an 2d array (<array>), scaled by <scale_ratio> for <seconds> seconds"""
	original_img1 = Image.new("RGB", (len(arr), len(arr[0])))
	original_img1.putdata(turn_2d_array_to_1d_arrayf(arr))
	display_img1 = original_img1.resize((len(arr)*scale_ratio, len(arr[0])*scale_ratio), Image.NEAREST)
	display_img1.save(temp_path)
	display_imgf(temp_path, seconds)
	os.remove(temp_path)
	return display_img1


def ensure_maze_save_path_exists():
	maze_save_path_exists = os.path.isdir(maze_save_path)
	
	if not maze_save_path_exists:
		os.makedirs(maze_save_path)


class Maze:
	def __init__(self, array2d, start_pos, end_pos):
		self.array2d = array2d
		self.start_pos = start_pos
		self.end_pos = end_pos

	def __str__(self):
		# return "This is a maze with the starting position {0} and the end position {1}..".format(str(self.number), str(self.generation))
		return "This is a maze with the starting position {0} and the end position {1}..".format(str(self.start_pos), str(self.end_pos))

	def __repr__(self):
		return "Maze(array2d = {0}, start_pos = {1}, end_pos = {2})".format(str(self.array2d), str(self.start_pos), str(len(self.end_pos)))

	def get_array2d(self):
		return self.array2d

	def get_start_pos(self):
		return self.start_pos

	def get_end_pos(self):
		return self.end_pos

	def set_array2d(self, array2d):
		self.array2d = array2d

	def set_start_pos(self, start_pos):
		self.start_pos = start_pos

	def set_end_pos(self, end_pos):
		self.end_pos = end_pos
	
	# Mazes print correctly for GAPathFinding.py.
	# TODO: Does it work for GAMazeGenerator.py?
	def print_asciified(self):
		maze_arr = self.get_array2d()
		for i in range(len(maze_arr)):
			for j in range(len(maze_arr[0])):
				if maze_arr[i][j] == COLOR_BLACK:
					maze_arr[i][j] = "▓"
				if maze_arr[i][j] == COLOR_WHITE:
					maze_arr[i][j] = "░"
				if maze_arr[i][j] == COLOR_GREEN:
					maze_arr[i][j] = "▒"
				if maze_arr[i][j] == COLOR_BLUE:
					maze_arr[i][j] = "▒"
				if maze_arr[i][j] == COLOR_RED:
					maze_arr[i][j] = "X"
				print(maze_arr[i][j], end='')
			print()
