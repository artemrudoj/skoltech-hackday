__author__ = 'artem'

import numpy as np
import csv

class Polygon:
    # looks like [[0,0],[0,1]]
    # center of polygone
    row_points = []
    points = []
    width = 0
    angles_count = 0
    layer = 0
    def __init__(self, row_points, width, layer):
        self.row_points = row_points
        self.width = width
        self.layer = layer
        self.angles_count = row_points.__len__()  * 2
        self.points = [None] * self.angles_count
    def __init__(self, cvs_line):
        self.width = 0.2
        self.layer = int(cvs_line[0])
        self.row_points = []
        self.points = []
        count_coordinates = cvs_line[1]
        index = 20
        for i in range(0, int(count_coordinates)):
            x = str(cvs_line[index]).replace(',','.')
            y = str(cvs_line[index + 1]).replace(',','.')
            self.row_points.append([float(x), float(y)])
            index = index + 2
        self.angles_count = self.row_points.__len__()  * 2
        self.points = [None] * self.angles_count

    def toString(self):
        assert (self.angles_count == self.points.__len__() )
        line = "POLY " + str(self.points.__len__() ) + ", " + str(self.layer) + "\n"
        for point in self.points:
            line = self.pointToString(point, line)
        return line

    def pointToString(self, point, line):
        line = line + str(point[0]).replace(".", ",") + "; " + str(point[1]).replace(".", ",") + '\n'
        return line

    def generatePolygone(self):
        self.makeEdgesOfPolygone()
        self.makeBodyOfPolygone()
        return

    def makeBodyOfPolygone(self):
        if self.row_points.__len__()  <=2:
            return
        for i in range(0, self.row_points.__len__()  - 2):
            equation_1 = self.generateLinearEquation(self.row_points[i], self.row_points[i+1],True)
            equation_2 = self.generateLinearEquation(self.row_points[i+1], self.row_points[i+2], True)
            x = self.solveLinearEqutaions(equation_1,equation_2)
            self.points[i + 1] = x

            equation_1 = self.generateLinearEquation(self.row_points[i], self.row_points[i+1],False)
            equation_2 = self.generateLinearEquation(self.row_points[i+1], self.row_points[i+2],False)
            x = self.solveLinearEqutaions(equation_1,equation_2)
            self.points[self.angles_count  - i - 2] = x
        return

    def makeEdgesOfPolygone(self):
        npArray = np.array(self.row_points)

        perpendicular = self.makePerpendicular(npArray[1] - npArray[0], self.width)
        self.points[0] = self.row_points[0] + perpendicular
        self.points[self.angles_count - 1] = self.row_points[0] - perpendicular

        perpendicular = self.makePerpendicular(npArray[self.row_points.__len__() - 1] - npArray[self.row_points.__len__() - 2],
                                               self.width)
        self.points[self.angles_count / 2 - 1] = self.row_points[self.row_points.__len__() - 1] + perpendicular
        self.points[self.angles_count / 2] = self.row_points[self.row_points.__len__() - 1] - perpendicular

    def generateLinearEquation(self, point_1, point_2, isPlus):
        point_1  = np.array(point_1)
        point_2  = np.array(point_2)
        perpendicular = self.makePerpendicular(point_2 - point_1, self.width)
        if isPlus:
            new_point_1 = point_1 + perpendicular
            new_point_2 = point_2 + perpendicular
        else :
            new_point_1 = point_1 - perpendicular
            new_point_2 = point_2 - perpendicular
        direction_vector = new_point_2 - new_point_1
        c = direction_vector[1]*new_point_1[0] - direction_vector[0]*new_point_1[1]
        equation = np.array([direction_vector[1], -direction_vector[0],c])
        return equation

    def solveLinearEqutaions(self, equation_1, equation_2):
        a = np.array([[equation_1[0],equation_1[1]],[equation_2[0],equation_2[1]]])
        b = np.array([equation_1[2],equation_2[2]])
        x = np.linalg.solve(a, b)
        return x

    def makePerpendicular(self, vector, width):
        x = vector[0]
        y = vector[1]
        vector[0] = y
        vector[1] = -x
        norma = np.linalg.norm(vector)
        a = vector / norma * width/2
        return a

def main():
    # polygone = Polygon([[5,3],[5,-1],[-2,-1],[-2,5],[2,5],[2,2]], 1,1)

    f = open("layers.csv", 'rt')
    solution = open("solution",'w')
    jumps = open("jumps.csv", 'rt')
    try:
        reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
        for row in reader:
            polygone = Polygon(row)
            polygone.generatePolygone()
            solution.write(polygone.toString())



        reader = csv.reader(jumps, quoting=csv.QUOTE_NONNUMERIC)
        for row in reader:
            solution.write( "JUMP " + row[1] + "; " + row[2] + "\n")

    finally:
        f.close()
        solution.close()
        jumps.close()

if __name__ == "__main__":
    main()
