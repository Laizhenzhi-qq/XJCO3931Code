# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 15:29:22 2020

@author: Administrator
"""
import numpy as np
import math
import random


def DD(la, mu, size):
    #print("Executing arguments value: lambda=",la,";mu=",mu,";size=",size)
    x = np.linspace(1, size, size)
    y = np.zeros(size,dtype=np.float32)
    for k in range(1,size):
        y[k] = -(1/la)*math.log(random.random())

    #serve distribution
    #Deterministic Distribution-----------------------------------------
    serve = np.zeros(size,dtype=np.float32)
    serve_i = 1
    for serve_i in range(1,size):
        serve[serve_i] = 1/mu
    
    #theory result
    Ws = (2 * mu - la)/(2 * mu * (mu - la))
    Wq = la/(2 * mu * (mu - la))
    Ls = (2 * mu * la - la * la)/(2 * mu * mu -(2 * la * mu))
    Lq = la * la / (2 * mu * (mu - la))
    #-------------------------------------------------------------------

    #arrive time
    t_arrive = np.zeros(size,dtype=np.float32)
    t_arrive[1] = y[1]
    total_arrive = np.zeros(size,dtype=np.float32)
    total_arrive [1] = 1
    arrive_i = 2
    for arrive_i in range(2,size):
        t_arrive[arrive_i] = t_arrive[arrive_i-1] + y[arrive_i]
        total_arrive[arrive_i] = arrive_i
        
    #leave time
    t_leave = np.zeros(size,dtype=np.float32)
    t_leave[1] = t_arrive[1] + serve[1]
    total_leave = np.zeros(size,dtype=np.float32)
    total_leave [1] = 1
    leave_i = 2
    for leave_i in range(2,size):
        if t_leave[leave_i-1]<t_arrive[leave_i]:
            t_leave[leave_i] = t_arrive[leave_i] + serve[leave_i]
        else:
            t_leave[leave_i] = t_leave[leave_i-1] + serve[leave_i]
            total_leave[leave_i] = leave_i

    #time line
    time_line = np.zeros(2*size,dtype=np.float32)
    num_line = np.zeros(2*size,dtype=np.float32)
    a = 1
    l = 1
    k = 1
    while(a<=size-1): 
        if(t_arrive[a]<t_leave[l]):
            a_count = 1        
            if(a <= size-2):
                while(t_arrive[a+1] == t_arrive[a]):
                    a_count = a_count + 1
                    a = a + 1
                    if(a == size-1):
                        break
            time_line[k] = t_arrive[a]
            num_line[k] = num_line[k-1] + a_count
            k = k + 1
            a = a + 1
            continue
        if(t_arrive[a]>=t_leave[l]):
            while(t_arrive[a] >= t_leave[l]):
                l_count = -1
                time_line[k] = t_leave[l]
                num_line[k] = num_line[k-1] + l_count
                k = k + 1
                if(l<size-1):
                    l = l + 1
    time_line[k] = t_leave[size-1]

    #simulating result
    sim_Ws = 0
    sim_Wq = 0
    sim_Ls = 0
    sim_Lq = 0
    Ws_line = np.zeros(size,dtype=np.float32)
    Wq_line = np.zeros(size,dtype=np.float32)
    total_Ls = 0
    total_Lq = 0
    total_Ws = 0
    total_Wq = 0
    for k in range(1,size):
        Ws_line[k] = t_leave[k] - t_arrive[k]
        total_Ws = total_Ws + Ws_line[k]
    sim_Ws = total_Ws/(size-1)


    for k in range(1,size):
        Wq_line[k] = t_leave[k] - t_arrive[k] - serve[k]
        total_Wq = total_Wq + Wq_line[k]
    sim_Wq = total_Wq/(size-1)


    for k in range (1,2*size):
        if(time_line[k+1] == 0):
            break
        total_Ls = num_line[k] * (time_line[k+1]-time_line[k]) + total_Ls
    sim_Ls = total_Ls/(t_leave[-1]-t_arrive[1])


    for k in range(1,2*size):
        if(time_line[k+1]==0):
            break
        if(num_line[k]>=2):
            total_Lq = (num_line[k] - 1) * (time_line[k+1]-time_line[k]) + total_Lq
    sim_Lq = total_Lq/(t_leave[-1]-t_arrive[1])
    
    sim_result = [sim_Ws, sim_Wq, sim_Ls, sim_Lq] 
    return sim_result

def NED(la, mu, size):
    #print("Executing arguments value: lambda=",la,";mu=",mu,";size=",size)
    x = np.linspace(1, size, size)
    y = np.zeros(size,dtype=np.float32)
    for k in range(1,size):
        y[k] = -(1/la)*math.log(random.random())

    #serve distribution
    #Negative Exponential Distribution-----------------------------------------
    serve = np.zeros(size,dtype=np.float32)
    for serve_i in range(1,size):
        serve[serve_i] = -(1/mu)*math.log(random.random())
    
    #theory result
    Ws = 1/(mu - la)
    Wq = la/(mu * (mu - la))
    Ls = la/(mu - la)
    Lq = la * la / (mu * (mu - la))
    #-------------------------------------------------------------------

    #arrive time
    t_arrive = np.zeros(size,dtype=np.float32)
    t_arrive[1] = y[1]
    total_arrive = np.zeros(size,dtype=np.float32)
    total_arrive [1] = 1
    arrive_i = 2
    for arrive_i in range(2,size):
        t_arrive[arrive_i] = t_arrive[arrive_i-1] + y[arrive_i]
        total_arrive[arrive_i] = arrive_i
        
    #leave time
    t_leave = np.zeros(size,dtype=np.float32)
    t_leave[1] = t_arrive[1] + serve[1]
    total_leave = np.zeros(size,dtype=np.float32)
    total_leave [1] = 1
    leave_i = 2
    for leave_i in range(2,size):
        if t_leave[leave_i-1]<t_arrive[leave_i]:
            t_leave[leave_i] = t_arrive[leave_i] + serve[leave_i]
        else:
            t_leave[leave_i] = t_leave[leave_i-1] + serve[leave_i]
            total_leave[leave_i] = leave_i

    #time line
    time_line = np.zeros(2*size,dtype=np.float32)
    num_line = np.zeros(2*size,dtype=np.float32)
    a = 1
    l = 1
    k = 1
    while(a<=size-1): 
        if(t_arrive[a]<t_leave[l]):
            a_count = 1        
            if(a <= size-2):
                while(t_arrive[a+1] == t_arrive[a]):
                    a_count = a_count + 1
                    a = a + 1
                    if(a == size-1):
                        break
            time_line[k] = t_arrive[a]
            num_line[k] = num_line[k-1] + a_count
            k = k + 1
            a = a + 1
            continue
        if(t_arrive[a]>=t_leave[l]):
            while(t_arrive[a] >= t_leave[l]):
                l_count = -1
                time_line[k] = t_leave[l]
                num_line[k] = num_line[k-1] + l_count
                k = k + 1
                if(l<size-1):
                    l = l + 1
    time_line[k] = t_leave[size-1]

    #simulating result
    sim_Ws = 0
    sim_Wq = 0
    sim_Ls = 0
    sim_Lq = 0
    Ws_line = np.zeros(size,dtype=np.float32)
    Wq_line = np.zeros(size,dtype=np.float32)
    total_Ls = 0
    total_Lq = 0
    total_Ws = 0
    total_Wq = 0
    for k in range(1,size):
        Ws_line[k] = t_leave[k] - t_arrive[k]
        total_Ws = total_Ws + Ws_line[k]
    sim_Ws = total_Ws/(size-1)


    for k in range(1,size):
        Wq_line[k] = t_leave[k] - t_arrive[k] - serve[k]
        total_Wq = total_Wq + Wq_line[k]
    sim_Wq = total_Wq/(size-1)


    for k in range (1,2*size):
        if(time_line[k+1] == 0):
            break
        total_Ls = num_line[k] * (time_line[k+1]-time_line[k]) + total_Ls
    sim_Ls = total_Ls/(t_leave[-1]-t_arrive[1])


    for k in range(1,2*size):
        if(time_line[k+1]==0):
            break
        if(num_line[k]>=2):
            total_Lq = (num_line[k] - 1) * (time_line[k+1]-time_line[k]) + total_Lq
    sim_Lq = total_Lq/(t_leave[-1]-t_arrive[1])
    
    sim_result = [sim_Ws, sim_Wq, sim_Ls, sim_Lq] 
    return sim_result


def ED(la, mu, size, el_k):
    #print("Executing arguments value: lambda=",la,";mu=",mu,";size=",size)
    x = np.linspace(1, size, size)
    y = np.zeros(size,dtype=np.float32)
    for k in range(1,size):
        y[k] = -(1/la)*math.log(random.random())

    #serve distribution
    #Erlang Distribution-----------------------------------------
    y_k = np.zeros(size,dtype=np.float32)
    for k in range(1,size):
        for i in range(0,el_k):
            y_k[k] = -(1/mu)*math.log(random.random()) + y_k[k]
    
    serve = np.zeros(size,dtype=np.float32)
    serve_i = 1
    for serve_i in range(1,size):
        serve[serve_i] = 1/el_k * y_k[serve_i]
    
    #theory result
    Ws = ((1+el_k)*la)/(2*el_k*mu*(mu-la)) + 1/mu
    Wq = ((1+el_k)*la)/(2*el_k*mu*(mu-la))
    Ls = ((1+el_k)*la*la)/(2*el_k*mu*(mu-la)) + la/mu
    Lq = ((1+el_k)*la*la)/(2*el_k*mu*(mu-la))
    #-------------------------------------------------------------------

    #arrive time
    t_arrive = np.zeros(size,dtype=np.float32)
    t_arrive[1] = y[1]
    total_arrive = np.zeros(size,dtype=np.float32)
    total_arrive [1] = 1
    arrive_i = 2
    for arrive_i in range(2,size):
        t_arrive[arrive_i] = t_arrive[arrive_i-1] + y[arrive_i]
        total_arrive[arrive_i] = arrive_i
        
    #leave time
    t_leave = np.zeros(size,dtype=np.float32)
    t_leave[1] = t_arrive[1] + serve[1]
    total_leave = np.zeros(size,dtype=np.float32)
    total_leave [1] = 1
    leave_i = 2
    for leave_i in range(2,size):
        if t_leave[leave_i-1]<t_arrive[leave_i]:
            t_leave[leave_i] = t_arrive[leave_i] + serve[leave_i]
        else:
            t_leave[leave_i] = t_leave[leave_i-1] + serve[leave_i]
            total_leave[leave_i] = leave_i

    #time line
    time_line = np.zeros(2*size,dtype=np.float32)
    num_line = np.zeros(2*size,dtype=np.float32)
    a = 1
    l = 1
    k = 1
    while(a<=size-1): 
        if(t_arrive[a]<t_leave[l]):
            a_count = 1        
            if(a <= size-2):
                while(t_arrive[a+1] == t_arrive[a]):
                    a_count = a_count + 1
                    a = a + 1
                    if(a == size-1):
                        break
            time_line[k] = t_arrive[a]
            num_line[k] = num_line[k-1] + a_count
            k = k + 1
            a = a + 1
            continue
        if(t_arrive[a]>=t_leave[l]):
            while(t_arrive[a] >= t_leave[l]):
                l_count = -1
                time_line[k] = t_leave[l]
                num_line[k] = num_line[k-1] + l_count
                k = k + 1
                if(l<size-1):
                    l = l + 1
    time_line[k] = t_leave[size-1]

    #simulating result
    sim_Ws = 0
    sim_Wq = 0
    sim_Ls = 0
    sim_Lq = 0
    Ws_line = np.zeros(size,dtype=np.float32)
    Wq_line = np.zeros(size,dtype=np.float32)
    total_Ls = 0
    total_Lq = 0
    total_Ws = 0
    total_Wq = 0
    for k in range(1,size):
        Ws_line[k] = t_leave[k] - t_arrive[k]
        total_Ws = total_Ws + Ws_line[k]
    sim_Ws = total_Ws/(size-1)


    for k in range(1,size):
        Wq_line[k] = t_leave[k] - t_arrive[k] - serve[k]
        total_Wq = total_Wq + Wq_line[k]
    sim_Wq = total_Wq/(size-1)


    for k in range (1,2*size):
        if(time_line[k+1] == 0):
            break
        total_Ls = num_line[k] * (time_line[k+1]-time_line[k]) + total_Ls
    sim_Ls = total_Ls/(t_leave[-1]-t_arrive[1])


    for k in range(1,2*size):
        if(time_line[k+1]==0):
            break
        if(num_line[k]>=2):
            total_Lq = (num_line[k] - 1) * (time_line[k+1]-time_line[k]) + total_Lq
    sim_Lq = total_Lq/(t_leave[-1]-t_arrive[1])
    
    sim_result = [sim_Ws, sim_Wq, sim_Ls, sim_Lq] 
    return sim_result
