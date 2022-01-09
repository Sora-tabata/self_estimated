import matplotlib.pyplot as plt
import math
from intersection_point import calculateIntersectionPoint
from crossing_number_algorithm import calculateCrossingNumberAlgorithm

def getLaserIntersectionPoint(laserPointA,laserPointB,field):
    """
    laserPointにはレーザーを表す線分を格納する 例:laserPointA = [1,1]
    laserPointAはLRFの原点を表す。
    fieldは複数の線分を表すリストである。
    例:field = [[[0,0],[0,20]],
         [[0,20],[20,20]],
         [[20,20],[20,0]],
         [[20,0],[0,0]]]
    """
    #LRFがフィールド内に存在するか念のため確認。
    if (not calculateCrossingNumberAlgorithm(laserPointA,field)):
        return False [0,0]
    
    distance = 0
    n = 0
    intersectionPoint = [0,0]
    
    #レーザーとフィールドの交点を探す。
    for i in range(len(field)):
        result, tempPoint = calculateIntersectionPoint\
                            (laserPointA,laserPointB,field[i][0],field[i][1])
        if (result):
            distance = math.sqrt((tempPoint[0] - laserPointA[0])**2 +\
                                 (tempPoint[1] - laserPointA[1])**2)
            intersectionPoint = tempPoint
            n = i
            break
    
    #もっとLRFと近い交点がないか調べる
    for i in range(n,len(field)):
        result, tempPoint = calculateIntersectionPoint\
                            (laserPointA,laserPointB,field[i][0],field[i][1])
        if (result):
            tempDistance = math.sqrt((tempPoint[0] - laserPointA[0])**2 +\
                                 (tempPoint[1] - laserPointA[1])**2)
            if (tempDistance < distance):
                distance = tempDistance
                intersectionPoint = tempPoint
                
    return True, intersectionPoint


if __name__ == '__main__':
    field = [[[0, 0], [0, 10]],
             [[0, 10], [3, 10]],
             [[3, 10], [3,7 ]],
             [[3,7], [7, 7]],
             [[7,7], [7, 10]],
             [[7,10],[10,10]],
             [[10,10],[10,0]],
             [[10,0],[0,0]]]
    
    pointA = [8,9]
    pointB = [-10,0]
    result, intersectionPoint = getLaserIntersectionPoint(pointA,pointB,field)
    
    #フィールドを描写
    for i in range(len(field)):
        plt.plot([field[i][0][0], field[i][1][0]],
                 [field[i][0][1], field[i][1][1]])
    #LRFのレーザーを描写
    plt.plot([pointA[0],pointB[0]], [pointA[1],pointB[1]])
    #交点を描写
    plt.scatter(intersectionPoint[0],intersectionPoint[1])
    