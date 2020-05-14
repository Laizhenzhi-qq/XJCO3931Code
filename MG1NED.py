# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 16:28:45 2020

@author: Administrator
"""

from Functions import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator

la = 0.2
mu = 0.6
size = 3000
repeat_size = 60
el_k = 3

repeat_results = np.zeros((4,repeat_size),dtype=np.float32)

#Ws:0  Wq:1  Ls:2  Lq:3
for k in range(0,repeat_size):
    temp = NED(la,mu,size)
    repeat_results[0][k] = temp[0]
    repeat_results[1][k] = temp[1]
    repeat_results[2][k] = temp[2]
    repeat_results[3][k] = temp[3]
    
#theory result
#NED----------------------------------------------------------------
Ws = 1/(mu - la)
Wq = la/(mu * (mu - la))
Ls = la/(mu - la)
Lq = (la * la) / (mu * (mu - la))
#-------------------------------------------------------------------


def Mystd(data, ave):
    sum_num = 0.0
    for num in data:
        sum_num = sum_num + (num - ave) * (num - ave)
#    result = cmath.sqrt(sum_num/len(data))
    result = (sum_num/len(data)) ** 0.5
    return result

def Myvar(data, ave):
    sum_num = 0.0
    for num in data:
        sum_num = sum_num + (num - ave) * (num - ave)
    result = sum_num/len(data)
    return result

#Confidence Interval
stlist = [Mystd(repeat_results[0], Ws), Mystd(repeat_results[1], Wq), Mystd(repeat_results[2], Ls), Mystd(repeat_results[3], Lq)]
error = []
n = repeat_size
for st in stlist:
    error.append(1.96*(st/(n ** 0.5)))


#results 
print("    Theory | Average of Repeat Simulation | Standard Deviation | Variance | CI Error")
print("Ws: %.4f " %Ws ,"            %.4f            " %np.mean(repeat_results[0]) ,"      %.4f      " %Mystd(repeat_results[0], Ws) ,"    %.4f " %Myvar(repeat_results[0], Ws), "   %.4f " %error[0])
print("Wq: %.4f " %Wq ,"            %.4f            " %np.mean(repeat_results[1]) ,"      %.4f      " %Mystd(repeat_results[1], Wq) ,"    %.4f " %Myvar(repeat_results[1], Wq), "   %.4f " %error[1])
print("Ls: %.4f " %Ls ,"            %.4f            " %np.mean(repeat_results[2]) ,"      %.4f      " %Mystd(repeat_results[2], Ls) ,"    %.4f " %Myvar(repeat_results[2], Ls), "   %.4f " %error[2])
print("Lq: %.4f " %Lq ,"            %.4f            " %np.mean(repeat_results[3]) ,"      %.4f      " %Mystd(repeat_results[3], Lq) ,"    %.4f " %Myvar(repeat_results[3], Lq), "   %.4f " %error[3])


#print(np.mean(repeat_results[1]))
#print(np.mean(repeat_results[2]))
#print(np.mean(repeat_results[3]))
#print(np.std(repeat_results[0],ddof=1))
#print(Mystd(repeat_results[0], Ws))
#print(Myvar(repeat_results[0], Ws))
#print("theoritic results: Ws:",Ws,"Wq:",Wq,"Ls:",Ls,"Lq: ",Lq)

#diagram
x = np.linspace(1, repeat_size, repeat_size)
Ws_line = np.zeros(repeat_size,dtype=np.float32)
for k in range(0,repeat_size):
    Ws_line[k] = Ws
Wq_line = np.zeros(repeat_size,dtype=np.float32)
for k in range(0,repeat_size):
    Wq_line[k] = Wq
Ls_line = np.zeros(repeat_size,dtype=np.float32)
for k in range(0,repeat_size):
    Ls_line[k] = Ls
Lq_line = np.zeros(repeat_size,dtype=np.float32)
for k in range(0,repeat_size):
    Lq_line[k] = Lq

plt.subplot(221)
ax1=plt.gca()
#ax1.yaxis.set_major_locator(MultipleLocator(0.05))
plt.title('Distribution for Ws')
plt.xlabel('Repeat num')
plt.ylabel('Value')
plt.plot(x,repeat_results[0],'r', linewidth=1, c='#00CED1')
plt.plot(x,Ws_line,'r', linewidth=1,c='#000000')
####
plt.subplot(222)
ax2=plt.gca()
#ax2.yaxis.set_major_locator(MultipleLocator(0.05))
plt.title('Distribution for Wq')
plt.xlabel('Repeat num')
plt.ylabel('Value')
plt.plot(x,repeat_results[1],'r', linewidth=1, c='#FFA07A')
plt.plot(x,Wq_line,'r',linewidth=1,c='#000000')
plt.show()
###
plt.subplot(223)
#ax3=plt.gca()
#ax3.yaxis.set_major_locator(MultipleLocator(0.05))
plt.title('Distribution for Ls')
plt.xlabel('Repeat num')
plt.ylabel('Value')
plt.plot(x,repeat_results[2],'r', linewidth=1, c='b')
plt.plot(x,Ls_line,'r',linewidth=1,c='#000000')
###
plt.subplot(224)
#ax4=plt.gca()
#ax4.yaxis.set_major_locator(MultipleLocator(0.05))
plt.title('Distribution for Lq')
plt.xlabel('Repeat num')
plt.ylabel('Value')
plt.plot(x,repeat_results[3],'r', linewidth=1, c='r')
plt.plot(x ,Lq_line,'r',linewidth=1,c='#000000')
plt.show()