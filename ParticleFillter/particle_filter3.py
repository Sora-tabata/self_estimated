import random
import math
from scipy.stats import norm
import matplotlib.pyplot as plt
import sys
sys.path.append('../LRFSimulator')
import simulator 
from laser_maker import getLaserAngles


class ParticleFilter():
    def __init__(self):
        self.particle = []
         
    def makeParticle(self,particleSize,average,standardDeviation):
        """
        particleSizeはパーティクルの個数
        averageはmakeParticle()時に各パーティクルが持つ平均値を格納する配列。
        standardDeviationはパーティクル初期化時に用いる正規分布の標準偏差を格納する配列。
        例えば、パーティクルにxy座標と角度を持たせる場合、averageとstandardDeviationは3つの要素を持つ配列
        """
        if (len(average) != len(standardDeviation)):
            return False
        
        for i in range(particleSize):
            temp = []
            for j in range(len(average)):
                #平均がaverage[j]、標準偏差がstandardDeviation[j]の正規分布から乱数を作成
                temp.append(random.normalvariate(average[j],standardDeviation[j]))
            self.particle.append(temp)
        return True
    
    def getParticle(self):
        return self.particle
    
    def estimate(self,likelihood):
        
        #加重平均を行うための準備
        likelihoodSum = 0
        for i in range(len(likelihood)):
            likelihoodSum += likelihood[i]
            
        #加重平均で推定値を算出
        estimatedState = [0] * len(self.particle[0]) #初期化？？
        for i in range(len(self.particle)):
            for j in range(len(self.particle[0])):
                estimatedState[j] += self.particle[i][j] * likelihood[i] / likelihoodSum
        
        return estimatedState
    
    def resample(self, likelihood, standardDeviation):
        likelihoodSum = 0
        for i in range(len(likelihood)):
            likelihoodSum += likelihood[i]
            
        #次の状態のパーティクルを層化サンプリングで選ぶ。
        particleSize = len(self.particle)
        sampledParticle = [[0]*len(self.particle[0]) for i in range(particleSize)]
        u = random.uniform(0,1) * likelihood[0] / likelihoodSum
        a = 1 / particleSize
        aSum = u
        weightSum = likelihood[0] / likelihoodSum
        n = 0;
        for i in range(particleSize):
            while aSum >= weightSum :
                n += 1
                if (len(likelihood) > n):
                    weightSum += likelihood[n] / likelihoodSum
                else:
                    break
                
            if (len(likelihood) <= n):
                break
            
            for j in range(len(self.particle[0])):
                sampledParticle[i][j] = random.normalvariate(self.particle[n][j],standardDeviation[j])
                
            aSum += a
            
        self.particle = sampledParticle
        
        
    

class LikelihoodCalculator():
    def __init__(self,standardDeviation):
        self.standardDeviation = standardDeviation #standardDeviation標準偏差
    def calculateLikelihood(self,observedDistance,observedAngle,particle,field):
        likelihood = []
        for i in range(len(particle)):
            result,simulatedDistance = simulator.getPointCloud2(particle[i][0:2],
                                        particle[i][2],observedAngle,field)
            temp = 0
            if result:
                for j in range(len(observedAngle)):
                    #正規分布を使って尤度を計算
                    temp += norm.pdf(observedDistance[j] - simulatedDistance[j],0,
                                     self.standardDeviation)
                likelihood.append(temp)
            else:
                likelihood.append(0)
        return likelihood
        

def showField(field,truePosition,estimatedPosition,enc,particle):
    """
    フィールド、真の位置、パーティクルの持つxy座標の情報を表示
    """
    for i in range(len(field)):
        plt.plot([field[i][0][0], field[i][1][0]],
                 [field[i][0][1], field[i][1][1]])
        
    x = []
    y = []
    for i in range(len(particle)):
        x.append(particle[i][0])
        y.append(particle[i][1])
    plt.scatter(x,y)
    plt.scatter(truePosition[0],truePosition[1],c = "red")
    plt.scatter(estimatedPosition[0],estimatedPosition[1],c = "yellow")
    plt.scatter(enc[0],enc[1],c = "orange")
    plt.show()

def showPointCloud(obseredAngles,observedDistance):
    for i in range(len(obseredAngles)):
        plt.scatter(math.cos(obseredAngles[i]) * observedDistance[i],
                    math.sin(obseredAngles[i]) * observedDistance[i])
    plt.show()
        
if __name__ == '__main__':
    pf = ParticleFilter();
    enc = [1.5, 3, math.pi/2]
    if pf.makeParticle(100,enc,[1,1,0.01]):
        print("true")
    
    
    truePosition = [1,4]
    trueAngle = math.pi/2.
    laserRange = math.pi / 2
    laserNumber = 10
    field = [[[0, 0], [0, 10]],
                 [[0, 10], [3, 10]],
                 [[3, 10], [3,7 ]],
                 [[3,7], [7, 7]],
                 [[7,7], [7, 10]],
                 [[7,10],[10,10]],
                 [[10,10],[10,0]],
                 [[10,0],[0,0]]]
    observedAngles = getLaserAngles(laserRange,laserNumber)
    result,observedDistance = simulator.getPointCloud2(truePosition,trueAngle,
                                                observedAngles,field)
    
    showPointCloud(observedAngles,observedDistance)
    lc = LikelihoodCalculator(1)
    
    
    for i in range(10):
        likelihood = lc.calculateLikelihood(observedDistance,observedAngles,
                                     pf.getParticle(),field)
        estimatedState = pf.estimate(likelihood)
        pf.resample(likelihood,[0.1,0.1,0.001])
        showField(field,truePosition,estimatedState[0:2],enc,pf.getParticle())