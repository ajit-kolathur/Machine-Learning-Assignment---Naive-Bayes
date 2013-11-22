__author__ = 'ajit'
import csv
import math

array = []
with open("./Weka/Assignment 1/train_test.csv", newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        if row[0] == 'letter':
            continue
        else:
            for i in range(1, 41):
                row[i] = int(row[i])
            array.append(row)
for i in range(0, len(array)):
    for j in range(3, len(array[i]), 2):
        array[i][j] = int(array[i][j-2]) - int(array[i][j])
        array[i][j+1] = int(array[i][j-1]) - int(array[i][j+1])
    centroid = [0, 0]
    for j in range(1, len(array[i]), 2):
        centroid[0] += int(array[i][j])
        centroid[1] += int(array[i][j+1])
    totalPoints = len(array[i]) - 1
    centroid[0] /= totalPoints
    centroid[1] /= totalPoints
    for j in range(1, len(array[i]), 2):
        array[i][j] -= centroid[0]
        array[i][j+1] -= centroid[1]
        radius = math.sqrt(array[i][j]**2 + array[i][j+1]**2)
        if array[i][j] == 0:
            theta = math.pi/2 * math.copysign(1, array[i][j+1])
        else:
            theta = math.atan(array[i][j+1] / array[i][j])
        array[i][j] = radius
        array[i][j+1] = theta
print("Cool Bro")
with open("parsed_output.csv", 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(array)