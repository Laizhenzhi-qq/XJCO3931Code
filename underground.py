# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 20:26:06 2020

@author: Administrator
"""
import math
import random
import numpy as np

running_time = 5400
la = 0.95581
la = la * 3
rate = 0.056
luggage_rate = 0.616
walk_time = 9
security_walk = 2.72
security_serve = 4.2
mu = 0.0251129
x = 20
serve2 = 1/0.237

class passenger(object):
    choice = 1
    luggage = 1
    t_arrive1 = 0.00
    t_leave1 = 0.00
    t_arrive2 = 0.00
    t_leave2 = 0.00
    t_serve1 = 0.00
    t_serve2 = 0.00
    temp_arrive = 0.00
    temp_leave = 0.00
    
    
def min_leave(server_plat):
    num = server_plat[0]
    index = 0
    for k in range(1,len(server_plat)):
        if num > server_plat[k]:
            index = k
            num = server_plat[k]
    return num, index
    
def min_len(server_plat):
    num = len(server_plat[0])
    index = 0
    for k in range(1,len(server_plat)):
        if num > len(server_plat[k]):
            index = k
            num = len(server_plat[k])
    return index

def max_len(server_plat):
    num = len(server_plat[0])
    for k in range(1,len(server_plat)):
        if num < len(server_plat[k]):
            num = len(server_plat[k])
    return num



def Initpassengers():

    #initialize and arrive time
    allpeople = []
    
    allpeople.append(passenger())
    size = 1
    
    while(True):
        t = allpeople[size-1].t_arrive1 - (1/la)*math.log(random.random())
        if(t < running_time):
            size = size + 1
            allpeople.append(passenger())
            allpeople[size-1].t_arrive1 = t
        else:
            break

    ################################################################
    #serve time 1 (NED)
    serve1 = np.zeros(size,dtype=np.float32)
    serve_y = np.zeros(size,dtype=np.float32)
    for k in range(1,size):
        serve_y[k] = -(1/mu)*math.log(random.random())
        
        serve_i = 1
    for serve_i in range(1,size):
        serve1[serve_i] = serve_y[serve_i] + x

    ###############################################################
    #server time 2 (DD)
    for person in allpeople:
        person.t_serve2 = serve2

    ###############################################################
    #initialize serve time and divide by choice
    for i in range(1,size):
        k1 = random.random()
        allpeople[i].t_serve1 = serve1[i]
        if k1 > rate:
            allpeople[i].choice = 2
        
        k2 = random.random()
        if k2 < luggage_rate:
            allpeople[i].luggage = 2
            
    return allpeople, size


def Undergroundsim(allpeople, size, platsize1, platsize2, X_raylength):
    ###############################################################
    #initialize server plat 1
    server_plat1 = []
    max_plat1 = 0
    for i in range(0,platsize1):
        server_plat1.append([])
        
    ###############################################################
    #leave time 1
    for person in allpeople:
        if person.choice == 1:
            now_time = person.t_arrive1
            for queue in server_plat1:
                if len(queue) != 0:
                    for obj in queue:
                        if obj.t_leave1 <= now_time:
                            queue.remove(obj)
        
            index = min_len(server_plat1)
            server_plat1[index].append(person)
            if max_plat1 < max_len(server_plat1):
                max_plat1 = max_len(server_plat1)
            
            if len(server_plat1[index]) == 1:
                person.t_leave1 = person.t_arrive1 + person.t_serve1
                person.temp_arrive = person.t_leave1 + walk_time
            else:
                person.t_leave1 = server_plat1[index][len(server_plat1[index])-2].t_leave1 + person.t_serve1
                person.temp_arrive = person.t_leave1 + walk_time
                
        else:
            person.t_leave1 = person.t_arrive1
            person.temp_arrive = person.t_leave1 + walk_time
        
    
    ###############################################################
    #security check
    security_queue = []
    
    for person in allpeople:
        if person.luggage == 1:
            person.temp_leave = person.temp_arrive + security_walk
            person.t_arrive2 = person.temp_leave
        else:
            now_time = person.temp_arrive
            index_count = 0
            for leave_time in security_queue:
                if leave_time <= now_time:
                    index_count = index_count + 1
            for i in range(0,index_count):
                security_queue.remove(security_queue[0])
            
            if len(security_queue) == 0:
                person.temp_leave = person.temp_arrive + security_serve
                person.t_arrive2 = person.temp_leave
                security_queue.append(person.temp_leave)
            else:
                person.temp_leave = security_queue[len(security_queue)-1] + (security_serve/X_raylength)
                person.t_arrive2 = person.temp_leave                
                security_queue.append(person.temp_leave)
    
    ###############################################################
    #initialize server plat 2
    server_plat2 = []
    max_plat2 = 0
    for i in range(0,platsize2):
        server_plat2.append([])
    
    ###############################################################
    #leave time 2
    for person in allpeople:
        now_time = person.t_arrive2
        for queue in server_plat2:
            if len(queue) != 0:
                for obj in queue:
                    if obj.t_leave2 <= now_time:
                        queue.remove(obj)
        
        index = min_len(server_plat2)
        server_plat2[index].append(person)
        if max_plat2 < max_len(server_plat2):
            max_plat2 = max_len(server_plat2)
            
        if len(server_plat2[index]) == 1:
            person.t_leave2 = person.t_arrive2 + person.t_serve2
        else:
            person.t_leave2 = server_plat2[index][len(server_plat2[index])-2].t_leave2 + person.t_serve2
           
        #if person.t_leave2 < person.t_arrive1:
        #    print('False')
        #    print(person.choice, person.luggage, person.t_arrive1, person.t_leave1, person.temp_arrive, person.temp_leave, person.t_arrive2, person.t_serve2)

    return allpeople, max_plat1, max_plat2
###############################################################
#test
'''
count = 0
for obj in allpeople:
    if obj.choice == 1:
        count = count + 1
print(count/size)
print(min_len(server_plat1))
for obj in allpeople:
    if obj.choice == 1:
        print(obj.t_arrive1,'-',obj.t_leave1,':',obj.t_leave1 - obj.t_arrive1 - obj.t_serve1,':',obj.t_serve1)
    #else:
       # print(obj.t_arrive2,'-',obj.t_leave2,':',obj.t_leave2 - obj.t_arrive2 - obj.t_serve2)
'''
