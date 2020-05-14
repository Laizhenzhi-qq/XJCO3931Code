# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 21:09:05 2020

@author: Administrator
"""

from underground import *
import copy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator

simlist = []
passengermodel = Initpassengers()
size = passengermodel[1]
model = copy.deepcopy(passengermodel[0])

x1 = []
x2 = [10, 11, 12, 13, 14, 15]
for obj in x2:
    x1.append(10)

combination = []
for m in range(0,len(x1)):
    combination.append([x1[m], x2[m]])
for comb in combination:
    simlist.append(Undergroundsim(copy.deepcopy(model), size, comb[0], comb[1], 8))


Ws0 = []
Ws1 = []
Ws2 = []
Wq0 = []
Wq1 = []
Wq2 = []
Ls0 = []
Ls1 = []
maxls1 = []
maxls2 = []
Ls2 = []
Lq0 = []
Lq1 = []
Lq2 = []
serve2 = 1/0.237

for obj in simlist:
    summ0 = 0
    summ1 = 0
    summ2 = 0
    count = 0
    for passenger in obj[0]:
        summ0 = summ0 + passenger.t_leave2 - passenger.t_arrive1
        if passenger.choice == 1:
            summ1 = summ1 + passenger.t_leave1 - passenger.t_arrive1
            count = count + 1
        summ2 = summ2 + passenger.t_leave2 - passenger.t_arrive2
    Ws0.append(summ0/size)
    Ws1.append(summ1/count)
    Ws2.append(summ2/size)
    Ls0.append(summ0/5400)
    Ls1.append(summ1/5400)
    Ls2.append(summ2/5400)

for obj in simlist:
    summ0 = 0
    summ1 = 0
    summ2 = 0
    count = 0
    for passenger in obj[0]:
        if passenger.choice == 1:
            summ0 = summ0 + passenger.t_leave2 - passenger.t_arrive1 - passenger.t_serve1 - passenger.t_serve2
            summ1 = summ1 + passenger.t_leave1 - passenger.t_arrive1 - passenger.t_serve1
            count = count + 1
        else:
            summ0 = summ0 + passenger.t_leave2 - passenger.t_arrive1 - passenger.t_serve2
        summ2 = summ2 + passenger.t_leave2 - passenger.t_arrive2 - passenger.t_serve2
    Wq0.append(summ0/size)
    Wq1.append(summ1/count)
    Wq2.append(summ2/size)
    Lq0.append(summ0/5400)
    Lq1.append(summ1/5400)
    Lq2.append(summ2/5400)
print("------Ws")
print('Ws0-',Ws0)
print('Ws1-',Ws1)
print('Ws2-',Ws2)
print("------Wq")
print('Wq0-',Wq0)
print('Wq1-',Wq1)
print('Wq2-',Wq2)
print("------Ls")
print('Ls0-',Ls0)
print('Ls1-',Ls1)
print('Ls2-',Ls2)
print("------Lq")
print('Lq0-',Lq0)
print('Lq1-',Lq1)
print('Lq2-',Lq2)

for obj in simlist:
    maxls1.append(obj[1])
    maxls2.append(obj[2])
print("------")
print("max queue length for ATMs:", maxls1)
print("max queue length for AFCs:", maxls2)


#diagrams
##################

##################
plt.subplot(221)
ax1=plt.gca()
ax1.xaxis.set_major_locator(MultipleLocator(1))
plt.title('Ws(ATMs)')
plt.xlabel('ATM Number')
plt.ylabel('Value')
plt.plot(x1,Ws0,'r', linewidth=1)
plt.plot(x1,Ws1,'r', linewidth=1, c='#00CED1')
####
plt.subplot(222)
ax2=plt.gca()
ax2.xaxis.set_major_locator(MultipleLocator(1))
plt.title('Wq(ATMs)')
plt.xlabel('ATM Number')
plt.ylabel('Value')
plt.plot(x1,Wq0,'r', linewidth=1)
plt.plot(x1,Wq1,'r', linewidth=1, c='#00CED1')
plt.show()
####
plt.subplot(221)
ax3=plt.gca()
ax3.xaxis.set_major_locator(MultipleLocator(1))
plt.title('Ls(ATMs)')
plt.xlabel('ATM Number')
plt.ylabel('Value')
plt.plot(x1,Ls0,'r', linewidth=1)
plt.plot(x1,Ls1,'r', linewidth=1, c='#00CED1')
####
plt.subplot(222)
ax4=plt.gca()
ax4.xaxis.set_major_locator(MultipleLocator(1))
plt.title('Lq(ATMs)')
plt.xlabel('ATM Number')
plt.ylabel('Value')
plt.plot(x1,Lq0,'r', linewidth=1)
plt.plot(x1,Lq1,'r', linewidth=1, c='#00CED1')
plt.show()
###################   

###################
plt.subplot(221)
ax5=plt.gca()
ax5.xaxis.set_major_locator(MultipleLocator(1))
plt.title('Ws(AFCs)')
plt.xlabel('AFC Number')
plt.ylabel('Value')
plt.plot(x2,Ws0,'r', linewidth=1)
plt.plot(x2,Ws2,'r', linewidth=1, c='#00CED1')
####
plt.subplot(222)
ax6=plt.gca()
ax6.xaxis.set_major_locator(MultipleLocator(1))
plt.title('Wq(AFCs)')
plt.xlabel('AFC Number')
plt.ylabel('Value')
plt.plot(x2,Wq0,'r', linewidth=1)
plt.plot(x2,Wq2,'r', linewidth=1, c='#00CED1')
plt.show()
####
plt.subplot(221)
ax7=plt.gca()
ax7.xaxis.set_major_locator(MultipleLocator(1))
plt.title('Ls(AFCs)')
plt.xlabel('AFC Number')
plt.ylabel('Value')
plt.plot(x2,Ls0,'r', linewidth=1)
plt.plot(x2,Ls2,'r', linewidth=1, c='#00CED1')
####
plt.subplot(222)
ax8=plt.gca()
ax8.xaxis.set_major_locator(MultipleLocator(1))
plt.title('Lq(AFCs)')
plt.xlabel('AFC Number')
plt.ylabel('Value')
plt.plot(x2,Lq0,'r', linewidth=1)
plt.plot(x2,Lq2,'r', linewidth=1, c='#00CED1')
