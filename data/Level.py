import os
import re


class Level:
    def __init__(self, name, width, height, raw_level):
        self.name = name
        self.width = int(width)
        self.height = int(height)
        self.raw_level = raw_level
        self.encoded_level = None
        self.padded_level = None

    def string_2d(self):
        return self.padded_level

    def string_1d(self):
        string = ""
        for line in self.padded():
            string += line + os.linesep
        return string

    def __str__(self):
        string = ""
        for line in self.padded():
            string += line + os.linesep
        return string

    def print_encoded(self):
        string = ""
        for line in self.encoded():
            string += str(line) + os.linesep
        print(string)

    def print_padded(self):
        string = ""
        for line in self.padded():
            string += str(line) + os.linesep
        print(string)

    def encoded(self):
        mapping = {'#': '1', '@': '2', '\+': '3', '\$': '4', '\*': '5', '\.': '6', ' ': '7', os.linesep: ''}

        if self.encoded_level is None:
            coded_maze = []
            for line in self.raw_level:
                for char in mapping:
                    line = re.sub(char, mapping[char], line)
                coded_maze.append(line)
            self.encoded_level = coded_maze
        return self.encoded_level

    def padded(self):
        if self.padded_level is None:
            blank_line = []
            for i in range(0, self.width + 2):
                blank_line.append(" ")

            field = [blank_line]

            for j in range(0, self.height):
                line = blank_line.copy()
                line_str = self.raw_level[j]
                line_arr = list(line_str)
                for i in range(0, len(line_arr)):
                    line[i + 1] = line_arr[i]
                field.append(line)

            field.append(blank_line)

            field = fill_neighbour(field, 0, 0)

            # cut borders
            new_list = []

            for i in range(1, self.height + 1):
                line = []
                for j in range(1, self.width + 1):
                    line.append(field[i][j])
                new_list.append(line)

            padded_field = []
            for line in new_list:
                line_str = "".join(line)
                padded_field.append(line_str)

            self.padded_level = padded_field

        return self.padded_level


def fill_neighbour(field, x, y):
    width = len(field)
    height = len(field[0])

    field[x][y] = '#'

    # check top neighbour
    if y != 0:
        if field[x][y - 1] == " ":
            field = fill_neighbour(field, x, y - 1)
    # check bottom neighbour
    if y != height - 1:
        if field[x][y + 1] == " ":
            field = fill_neighbour(field, x, y + 1)
    # check left neighbour
    if x != 0:
        if field[x - 1][y] == " ":
            field = fill_neighbour(field, x - 1, y)
    # check right neighbour
    if x != width - 1:
        if field[x + 1][y] == " ":
            field = fill_neighbour(field, x + 1, y)

    return field
