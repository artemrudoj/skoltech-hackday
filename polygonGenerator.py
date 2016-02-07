__author__ = 'artem'

import numpy as np


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
    def toString(self):
        assert (self.angles_count == self.points.__len__() )
        line = "POLY " + str(self.points.__len__() ) + ", " + str(self.layer) + "\n"
        for point in self.points:
            line = self.pointToString(point, line)
        return line

    def pointToString(self, point, line):
        line = line + str(point[0]) + "; " + str(point[1]) + '\n'
        return line

    def generatePolygone(self):
        self.makeEdgesOfPolygone()
        self.makeBodyOfPolygone()
        return

    def makeBodyOfPolygone(self):
        if (self.row_points.__len__()  <=2):
            return
        for i in range(0, self.row_points.__len__()  - 3):
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
        perpendicular = self.makePerpendicular(point_1 - point_2, self.width)
        if isPlus:
            new_point_1 = point_1 + perpendicular
            new_point_2 = point_2 + perpendicular
        else :
            new_point_1 = point_1 - perpendicular
            new_point_2 = point_2 - perpendicular
        direction_vector = new_point_2 - new_point_1
        c = direction_vector[0]*new_point_1[0] + direction_vector[1]*new_point_1[1]
        equation = np.array([direction_vector[0], direction_vector[1],c])
        return equation

    def solveLinearEqutaions(self, equation_1, equation_2):
        a = np.array([[equation_1[0],equation_2[0]],[equation_1[1],equation_2[1]]])
        b = np.array([equation_1[0],equation_2[0]])
        x = np.linalg.solve(a, b)
        return x

    def makePerpendicular(self, vector, width):
        x = vector[0]
        y = vector[1]
        if -y > 0:
            vector[0] = -y
            vector[1] = x
        else:
            vector[0] = y
            vector[1] = -x
        norma = np.linalg.norm(vector)
        a = vector / norma * width
        return a

def main():
    polygone = Polygon([[0,0],[1,1]], 1,1)
    polygone.generatePolygone()
    print( polygone.toString())

if __name__ == "__main__":
    main()