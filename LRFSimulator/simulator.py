import math
import matplotlib.pyplot as plt

from crossing_number_algorithm import calculateCrossingNumberAlgorithm
from laser_maker import getLaserAngles,getLasers
from coordinateConverter import convertCoordinate
from laser_intersection_point import getLaserIntersectionPoint


def getPointCloud(lrfPoint,lrfAngle,laserNumber,laserRange,field):
    '''
    lrfPoint = LRFの位置
    lrfAngle = LRFが置かれている角度
    laserNumber = レーザーの本数
    laserRange = レーザーの照射範囲
    field = フィールドを表すリスト
    この関数が適切に処理を行えなかった場合、Falseと空のリストを返す。
    この関数が適切に処理を行えた場合、Trueと点群を表すリストを返す。
    '''
    
    #LRFがフィールド内に存在するか判定
    if (not calculateCrossingNumberAlgorithm(lrfPoint,field)):
        return False,[]
    
    #この値は大きくしましょう
    laserLength = 10000     
    
    #レーザーを生成
    lasers = getLasers(getLaserAngles(laserRange,laserNumber),laserLength)
    lasers = convertCoordinate(lasers,lrfAngle,lrfPoint)
    
    #レーザーとフィールドの交点を求め、点群を生成する
    pointCloud = []
    for i in range(len(lasers)):
        result , point = getLaserIntersectionPoint(lrfPoint,lasers[i],field)
        pointCloud.append(point)
    
    return True, pointCloud
    
def getPointCloud2(lrfPoint,lrfAngle,laserAngles,field):
    '''
    lrfPoint = LRFの位置
    lrfAngle = LRFが置かれている角度
    laserNumber = レーザーの本数
    laserRange = レーザーの照射範囲
    field = フィールドを表すリスト
    この関数が適切に処理を行えなかった場合、Falseと空のリストを返す。
    この関数が適切に処理を行えた場合、Trueと点群を表すリストを返す。
    '''
    
    #LRFがフィールド内に存在するか判定
    if (not calculateCrossingNumberAlgorithm(lrfPoint,field)):
        return False,[]
    
    #この値は大きくしましょう
    laserLength = 10000     
    
    #レーザーを生成
    lasers = getLasers(laserAngles,laserLength)
    lasers = convertCoordinate(lasers,lrfAngle,lrfPoint)
    
    #レーザーとフィールドの交点を求め、点群を生成する
    pointCloud = []
    for i in range(len(lasers)):
        result , point = getLaserIntersectionPoint(lrfPoint,lasers[i],field)
        pointCloud.append(point)
        
    distance = []
    for i in range(len(lasers)):
        distance.append(math.sqrt(abs((lrfPoint[0] - pointCloud[i][0])**2 +
                                      (lrfPoint[1] - pointCloud[i][1])**2)))
    return True, distance  
    
if __name__ == '__main__':
    
    lrfPoint = [1,5]
    lrfAngle = math.pi/3
    laserNumber = 10
    laserRange = math.pi
    field = [[[0, 0], [0, 10]],
                 [[0, 10], [3, 10]],
                 [[3, 10], [3,7 ]],
                 [[3,7], [7, 7]],
                 [[7,7], [7, 10]],
                 [[7,10],[10,10]],
                 [[10,10],[10,0]],
                 [[10,0],[0,0]]]
    
    result ,pointCloud = getPointCloud(lrfPoint,lrfAngle,laserNumber,
                                       laserRange,field)
    
    #問題なく点群を生成できた場合
    if (result):
        #フィールドを描写
        for i in range(len(field)):
            plt.plot([field[i][0][0], field[i][1][0]],
                     [field[i][0][1], field[i][1][1]])
        #レーザーを描写
        for point in pointCloud :
            plt.plot([lrfPoint[0],point[0]],
                     [lrfPoint[1],point[1]])
            plt.scatter(point[0],point[1])
        
