__author__ = 'ajit'
# Bayesian learning on the data;
# TODO: Process the training data to obtain the intelligence, Bayesian Learning
# TODO: Dump intelligence file for testing
# Assignment 1: Vishwajit Kolathur Nov 12th 2013

import fileinput


class CharData:
    """A class to hold the (dx,dy)'s 20 of them, this assumes that the start is at (0,0)"""
    def __init__(self):
        self.letter = ''
        self.points = []

    def initialize(self, letter):
        self.letter = letter

    def insert(self, point):
        if len(self.points) <= 20:
            self.points.append(point)
        else:
            print("Too Many points")

    def access(self, i):
        if i < 20:
            return self.points[i]
        else:
            print("Out of Bounds error")

    def letter(self):
        return self.letter


def takeinput(file_name, array):
    with open(file_name, encoding='utf-8') as train_file:
        temp = ""
        for a_line in train_file:
            words = a_line.split()
            if words[0] == "label":
                if temp != "":
                    array.append(temp)
                temp = CharData()
                temp.initialize(words[1])
                print(words[1])
                continue
            else:
                dx_cords = words[::2]
                dy_cords = words[1::2]
                if len(dx_cords) != len(dy_cords):
                    print("ERROR in number of entries")
                for i in range(len(dx_cords)):
                    temp.insert((dx_cords[i], dy_cords[i]))
                    print((dx_cords[i], dy_cords[i]))
        array.append(temp)
def main():
    traindata = []
    takeinput('./Data/test.txt', traindata)
    print(traindata)


if __name__ == "__main__":
    main()