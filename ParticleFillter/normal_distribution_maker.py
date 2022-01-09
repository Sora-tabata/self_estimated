import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

#-5から5まで、0.01間隔で入ったリストXを作る
X = np.arange(-5,5,0.01)
#平均0、標準偏差の正規分布を作成
Y = norm.pdf(X,0,1)

#x,yを引数にして、関数の色をr(red)に指定
plt.plot(X,Y,color='r')
plt.show()