__author__ = 'artem'
import polygonGenerator

import matplotlib.pyplot as plt






def main():

    polygone = polygonGenerator.Polygon([[0,0],[0,1],[2,1]], 1,1)
    polygone.generatePolygone()
    # plt.plot([1,2,3,4], [1,4,9,16], 'ro')
    # plt.axis([0, 6, 0, 20])
    # plt.show()
    print( polygone.toString())

if __name__ == "__main__":
    main()