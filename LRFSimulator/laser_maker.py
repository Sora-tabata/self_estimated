import math
import matplotlib.pyplot as plt


def getLaserAngles(laserRange, laserNumber):
    """
    レーザーがなす角度を返す。
    laserRangeでレーザーの照射範囲を指定。
    laserNumberがレーザーの本数。
    """
    laserAngles = []
    for i in range(laserNumber):
        laserAngles.append(laserRange*(-1/2) + laserRange/(laserNumber-1)*i)
    return laserAngles

def getLasers(laserAngles,laserLength):
    """
    レーザーの放射先のxy座標を返す。
    laserAnglesはgetLaserAngles関数で求めたリスト。
    laserLengthはレーザーの長さ。
    """
    lasers = []
    for i in range(len(laserAngles)):
        lasers.append([math.cos(laserAngles[i])*laserLength,
                       math.sin(laserAngles[i])*laserLength])
    return lasers

if __name__ == '__main__':
    #math.piは円周率
    laserAngles = getLaserAngles(math.pi,5)
    lasers = getLasers(laserAngles,1000)
    
    print(laserAngles)
    
    for i in range(len(lasers)):
        plt.plot([0,lasers[i][0]], [0,lasers[i][1]])
        plt.scatter(lasers[i][0],lasers[i][1])


