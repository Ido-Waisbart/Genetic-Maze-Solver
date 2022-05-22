from PIL import Image
import random
import tkinter
import os

color_black = (0, 0, 0)
color_white = (255, 255, 255)
color_green = (0, 255, 0)  # start pos
color_blue = (0, 0, 255)  # end pos
color_red = (255, 0, 0)  # player
maze_size_x = 32
maze_size_y = 32
maze_size = (maze_size_x, maze_size_y)
display_ratio = 8
display_size = (maze_size_x*display_ratio, maze_size_y*display_ratio)
temp_path = "C:\\Users\\magshimim\\Documents\\Art\\genetic\\temp.png"
maze_save_path = "C:\\Users\\magshimim\\Documents\\Art\\genetic\\mazes\\"
OK_BLUE = '\033[94m'
END_C = '\033[0m'


# V DONE!
def display_imgf(save_path, second_amount):
	"""The function displays an image, which's path is <save_path>, in a separate window for <second_amount> seconds"""
	root = tkinter.Tk("Image display!")
	second = 1000
	display_time = int(second_amount * second)
	label_display_img1 = tkinter.PhotoImage(file=save_path)
	img_label = tkinter.Label(root, image=label_display_img1)
	img_label.label_display_img1 = label_display_img1
	img_label.pack()
	if second_amount != 0:
		root.after(display_time, lambda: root.destroy())
	root.configure(background='slategray1')
	root.lift()
	root.geometry('%dx%d+%d+%d' % (display_size[0], display_size[1], 0, 0))
	root.mainloop()


# V DONE! (Unused)
def random_range(num_range):
	"""The function returns a sequence of random numbers in the number range <num_range>"""
	# Range = (0, 7)/(1, 9)/7
	random_range_list = []
	if type(num_range) == int:
		length = num_range
		for num in range(length):
			rand_num = random.randrange(0, num_range)
			while rand_num in random_range_list:
				rand_num = random.randrange(0, num_range)
			random_range_list.append(rand_num)
	elif type(num_range) == tuple and len(num_range) == 2 and type(num_range[0]) == int and type(num_range[1]) == int:
		length = num_range[1] - num_range[0]
		for num in range(length):
			rand_num = random.randrange(num_range[0], num_range[1])
			while rand_num in random_range_list:
				rand_num = random.randrange(num_range[0], num_range[1])
			random_range_list.append(rand_num)
	else:
		raise Exception("random_range() must have an int variable or a tuple of 2 ints")
	return random_range_list


# V DONE!
def turn_2d_array_to_1d_arrayf(array):
	"""The function turns a 2d array (array) to a 1d array"""
	maze_1darray = []
	for y in range(maze_size_y):
		for x in range(maze_size_x):
			maze_1darray.append(array[x][y])
	return maze_1darray


# V DONE!
def display_2d_arrayf(arr, scale_ratio, seconds):
	"""The function displays an 2d array (<array>), scaled by <scale_ratio> for <seconds> seconds"""
	original_img1 = Image.new("RGB", (len(arr), len(arr[0])))
	original_img1.putdata(turn_2d_array_to_1d_arrayf(arr))
	display_img1 = original_img1.resize((len(arr)*scale_ratio, len(arr[0])*scale_ratio))
	display_img1.save(temp_path)
	display_imgf(temp_path, seconds)
	os.remove(temp_path)
	return display_img1


# V DONE! (Unused)
def random_2darrayf(size_x, size_y):
	"""The function creates a 2d array with random black/white colors and with the size of <size_x> by <size_y>"""
	maze_2d_array = []
	for x in range(size_x):
		maze_2d_array.append([])
		for y in range(size_y):
			random_num = random.randrange(2)
			if random_num == 0:
				maze_2d_array[x].append(color_black)
			else:
				maze_2d_array[x].append(color_white)
	return maze_2d_array


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
