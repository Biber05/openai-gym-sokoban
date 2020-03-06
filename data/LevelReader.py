import os
import re
import xml.etree.ElementTree as ET

from Level import Level


class LevelReader:
    def __init__(self, path: str):
        self.path = path
        self.levels = []
        self.levels = self.import_levels_from_xml(path)

    def import_levels_from_xml(self, folder):
        files = os.listdir(folder)
        for f in files:
            path = os.path.join(folder, f)
            print(path)
            original_file_name = re.sub(".txt", "", f)
            tree = ET.parse(path)
            root = tree.getroot()
            level_collection = root.find("LevelCollection").getchildren()
            level_num = 0

            for level in level_collection:
                level_num = level_num + 1
                level_name = original_file_name + "_" + str(level_num)
                width = level.items()[1][1]
                height = level.items()[2][1]
                raw_level = []
                lines = level.getchildren()
                for line in lines:
                    raw_level.append(line.text)

                new_level = Level(level_name, width, height, raw_level)
                self.levels.append(new_level)
        return self.levels

    def smaller_levels_padded(self, width, height):
        new_list = []

        for level in self.levels:
            if level.width < width and level.height < height:
                # pad level to given size
                # 1. init new field
                new_field = []
                empty_line = ""
                for i in range(0, width):
                    empty_line += "#"
                for i in range(0, height):
                    new_field.append(list(empty_line))

                for i in range(0, level.height):
                    level_line = list(level.padded()[i])
                    for j in range(0, level.width):
                        new_field[i][j] = level.padded()[i][j]

                new_level = Level(level.name, width, height, new_field)
                new_list.append(new_level)
        return new_list

    def levels_2d_string(self):
        new_list = []
        for level in self.levels:
            new_list.append(level.string_2d())
        return new_list

    def levels_1d_string(self):
        new_list = []
        for level in self.levels:
            new_list.append(level.string_1d())
        return new_list


if __name__ == '__main__':
    reader = LevelReader("./0_raw")  # TEST_DIR
    print(len(reader.levels))
    levels = reader.smaller_levels_padded(10, 10)

    for i, l in enumerate(levels):

        with open("./1_padded/{}.txt".format(i), "w") as file:
            file.write(";1 \n")
            for item in l.padded():
                file.write("%s\n" % item)
