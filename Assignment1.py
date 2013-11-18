__author__ = 'ajit'
# Bayesian learning on the data;
# Assignment 1: Vishwajit Kolathur Nov 12th 2013

import operator
import math

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

    def directionalize(self):
        for i in range(len(self.points)):
            point = self.points[i]
            temp = ""
            if point[0] > 0:
                temp += "S"
            elif point[0] < 0:
                temp += "N"
            if point[1] > 0:
                temp += "E"
            elif point[1] < 0:
                temp += "W"
            if temp == "":
                temp = "O"
            #if point == (0, 0):
            #    temp = 0
            #elif point[1] == 0:
            #    temp = 0
            #else:
            #    temp = 1 * math.atan(point[0]/point[1])
            self.points[i] = temp

    def sort_points(self):
        self.points.sort(key=lambda val: val[1])
        self.points.sort(key=lambda val: val[0])

    def convert_to_points(self):
        for i in range(len(self.points)):
            if i == 0:
                self.points[i] = tuple(map(operator.add, self.points[i], (0,0)))
            else:
                self.points[i] = tuple(map(operator.add, self.points[i], self.points[i-1]))


def take_input(file_name, array):
    with open(file_name, encoding='utf-8') as train_file:
        temp = ""
        for a_line in train_file:
            words = a_line.split()
            if len(words) == 0:
                continue
            if words[0] == "label":
                if temp != "":
                    array.append(temp)
                temp = CharData()
                temp.initialize(words[1])
                continue
            else:
                dx_cords = words[::2]
                dy_cords = words[1::2]
                if len(dx_cords) != len(dy_cords):
                    print("ERROR in number of entries")
                for i in range(len(dx_cords)):
                    temp.insert((int(dx_cords[i]), int(dy_cords[i])))
        array.append(temp)


def test_classify(train_data, test_data):
    classify = 0
    miss_classify = 0
    for test in test_data:
        probabilities = {}
        for alphabet in "abcdefghijklmnopqrstuvwxyz":
            items = [item for item in train_data if item.letter == alphabet]
            probabilities[alphabet] = len(items)/len(train_data)
            for i in range(0, 20):
                pattern_match = 0;
                for item in items:
                    if item.points[i] == test.points[i]:
                        pattern_match += 1
                pattern_match /= len(items)
                probabilities[alphabet] *= pattern_match
        if max(probabilities, key=probabilities.get) == test.letter:
            classify += 1
        else:
            miss_classify += 1
    classify, miss_classify = classify/(miss_classify + classify), miss_classify/(miss_classify + classify)

    print("Classification Rate: " + str(classify))
    print("MissClassification Rate: " + str(miss_classify))


def sort_inputs(train_data):
    for element in train_data:
        element.sort_points()


def set_directions(train_data):
    for data in train_data:
        data.directionalize()


def del_to_points(train_data):
    for data in train_data:
        data.convert_to_points()


def main():
    train_data = []
    test_data = []
    print("Starting Reading")
    take_input('./Data/A1_training.txt', train_data)
    take_input('./Data/A1_testing.txt', test_data)
    print("Reading Done")
    print("Start Normalizing")
    del_to_points(train_data)
    del_to_points(test_data)
    sort_inputs(train_data)
    sort_inputs(test_data)
    #set_directions(train_data)
    #set_directions(test_data)
    print("Normalizing Done")
    print("Starting Testing")
    test_classify(train_data, test_data)
    print("Testing Done")

if __name__ == "__main__":
    main()