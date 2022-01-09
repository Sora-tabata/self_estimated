import math
import matplotlib.pyplot as plt
import laser_maker 

def rotatePosition(position, angle):
    """
    xy座標を持つpositionをangle[rad]回転させる。
    """
    return [position[0]*math.cos(angle) - position[1]*math.sin(angle),
            position[0]*math.sin(angle) + position[1]*math.cos(angle)]
    
def convertCoordinate(lasers,angle,position):
    """
    angle[rad]回転させた後に、positon分平行移動させる。
    angleがLRFを置いた角度、positionがLRFの位置座標
    lasersは複数のxy座標データ持つ2次元リスト
    """
    result = []
    for i in range(len(lasers)):
        tempPosition = rotatePosition(lasers[i],angle)
        result.append([tempPosition[0] + position[0],
                       tempPosition[1] + position[1]])
    return result

if __name__ == '__main__':
    laserAngles = laser_maker.getLaserAngles(math.pi,5)
    lasers = laser_maker.getLasers(laserAngles,1000)
    
    LRFPosition = [400,400]
    LRFAngle = math.pi/3
    lasers = convertCoordinate(lasers,LRFAngle,LRFPosition)
    
    for i in range(len(lasers)):
        plt.plot([LRFPosition[0],lasers[i][0]], [LRFPosition[1],lasers[i][1]])
        plt.scatter(lasers[i][0],lasers[i][1])
