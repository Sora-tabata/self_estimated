import matplotlib.pyplot as plt
from intersection_point import calculateIntersectionPoint

def calculateCrossingNumberAlgorithm(point, field):
    """
    pointがfieldの内側にいる場合Trueを返す。
    pointがfieldの外側にいる場合Falseを返す。
    pointはxy座標を表す点。
    fieldは複数の線分を表す3次元のリスト。
    """
    #x座標の正方向に向けてpoint2を作成する。
    #ここの100000という数字はfieldの大きさに合わせて設定する必要がある。
    point2 = [100000 ,point[1]]
    intersectionPointNumber = 0
    #フィールドの各線分とpointとpoint2の線分の交点の数を数える
    for i in range(len(field)):
        result , intersectionPoint = \
            calculateIntersectionPoint(point,point2,field[i][0],field[i][1])
        if result:
            intersectionPointNumber += 1
            
    if intersectionPointNumber%2 == 1:
        return True
    else :
        return False
        
if __name__ == '__main__':
    field = [[[0, 0], [0, 10]],
             [[0, 10], [3, 10]],
             [[3, 10], [3,7 ]],
             [[3,7], [7, 7]],
             [[7,7], [7, 10]],
             [[7,10],[10,10]],
             [[10,10],[10,0]],
             [[10,0],[0,0]]]
    
    pointA = [1,8]
    print(calculateCrossingNumberAlgorithm(pointA,field))
    
    #フィールドを描写
    for i in range(len(field)):
        plt.plot([field[i][0][0], field[i][1][0]],
                 [field[i][0][1], field[i][1][1]])
    #点を描写
    plt.scatter(pointA[0],pointA[1])