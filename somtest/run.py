# -*- coding: UTF-8 -*-
import numpy as np
import matplotlib.pylab as plt
from time import time
from mysm import Mysm

a,b,c,d = np.loadtxt('data1.txt', delimiter='\t',usecols=(0,1,2,3),dtype='str',unpack=True)

length = a.size


#数据分割
i=0

while(i<length):
    tmp = a[i].split(': ')
    a[i] = tmp[2]
    i = i+1
i=0

while(i<length):
    tmp = b[i].split(': ')
    b[i] = tmp[1]
    i = i+1

i=0

while(i<length):
    tmp = c[i].split(': ')
    c[i] = tmp[1]
    i = i+1

i=0

while(i<length):
    tmp = d[i].split(': ')
    d[i] = tmp[1]
    i = i+1

#列合并
data_pre = np.column_stack((a,b,c,d))
data_preN = np.column_stack((b,c,d))
data_preN = data_preN.astype(float)
names = ['ftime', 'btime', 'cnt']

#上面全是读取数据


#数据归一化,感觉不用了
'''
max_val=np.max(data_preN,axis=0)
min_val=np.min(data_preN, axis=0)
#data = (data_preN-min_val)/(max_val-min_val)
me =np.mean(data_preN, axis=0)
st = np.std(data_preN,axis=0)
data = (data_preN-me)/st
'''
fig = plt.figure()
data = data_preN
plt.plot(data[:,0],data[:,1],'ob',alpha=0.2, markersize=4)
fig.set_size_inches(7,7)
#plt.show()
plt.savefig('zg107')

som = Mysm(data=data,names=names)
som.easytest()

print('ending...')

