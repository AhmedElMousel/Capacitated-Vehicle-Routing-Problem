# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 13:54:24 2020

@author: ElMousel
"""

import functools , operator , os , pandas , math , random , numpy , copy , matplotlib.pyplot as plt
import time
start_time = time.time()
xls =pandas.ExcelFile('F:\Data\datafile.xlsx')
sheet1 = pandas.read_excel(xls,'Sheet1')
sheet2 = pandas.read_excel(xls,'Sheet2')
nodes = sheet1.as_matrix()
depot = nodes[len(nodes)-1]
cities = nodes[:len(nodes)-1]
vehicle = sheet2.as_matrix()
tour =random.sample(range(len(cities)),len(cities))
n=len(cities)
numpy.seterr(divide="ignore")
def distance(x1,y1,x2,y2):
    return math.sqrt((x1-x2)**2+(y1-y2)**2)
def totaldistancetour(t):
    d=0
    for i in range(1,len(t)):
        x1 = cities[t[i-1]][0]
        y1 = cities[t[i-1]][1]
        x2 = cities[t[i]][0]
        y2 = cities[t[i]][1]
        d = d+distance(x1,y1,x2,y2)
    x1 = cities[t[len(t)-1]][0]
    y1 = cities[t[len(t)-1]][1]
    x2 = depot[0]
    y2 = depot[1]
    d = d+distance(x1,y1,x2,y2)
    x1 = cities[t[0]][0]
    y1 = cities[t[0]][1]
    x2 = depot[0]
    y2 = depot[1]
    d = d+distance(x1,y1,x2,y2)
    return d
def subtourslice(t , vehicle):
    capacityused = numpy.zeros(len(vehicle))
    k = 0
    slice=[]
    mass=[]
    x=0
    for i in range(len(vehicle)):
       
        while capacityused[x] <= vehicle[x][1] and k <= (len(t)-1):
            capacityused[x]=capacityused[x]+cities[t[k]][2]
            if capacityused[x] > vehicle[x][1]:
                capacityused[x]=capacityused[x]-cities[t[k]][2]
                k = k-1
                slice.append(k)
                k = k+1
                break
            k=k+1
        mass.append(capacityused[x])
        x=x+1
    slice.append(k-1)
    return slice,mass
def subtour(slice,t):
    sub=[]
    sub.append(t[:(slice[0]+1)])
    for i in range (0,len(slice)-1):
        sub.append(t[(slice[i]+1):(slice[i+1]+1)])
    return sub
def allvehicledistance(sub):
    alldistance = functools.reduce(operator.add,(totaldistancetour(x) for x in sub) , 0)
    return alldistance
def tourtodistance(t,vehicle):
    u=subtourslice(t,vehicle)
    v=subtour(u[0],t)
    total=allvehicledistance(v)
    return total
print "The intial distance is : ",tourtodistance(tour,vehicle)
def SAgetN(tourr):
    u=subtourslice(tourr,vehicle)[0]
    v=subtour(u,tourr)
    i=numpy.random.randint(0,len(v))
    ii=numpy.random.randint(0,len(v))
    while ii==i:
       ii=numpy.random.randint(0,len(v))
    j=numpy.random.randint(0,len(v[i]))
    jj=numpy.random.randint(0,len(v[ii]))
    A1=v[i][j]
    A2=v[ii][jj]
    tempTour=[]
    w=0
    for i in tourr:
        if tourr[w]==A1:
            tempTour.append(A2)
        elif tourr[w]==A2:
            tempTour.append(A1)
        else:
            tempTour.append(tour[w])
        w=w+1
    tempTour=list(tempTour)
    return tempTour
def GA(b):
    mutation=[]
    A1=numpy.random.randint(len(b))
    A2=numpy.random.randint(len(b))
    while A1== A2:
        A2=numpy.random.randint(len(b))
    if A1<A2 :
        A2=A2+1
        r1=copy.copy(b)
        r2=list(reversed(b[A1:A2]))
        t=0
        for i in range(A1,A2):
            r1[i]=r2[t]
            t=t+1
        mutation=copy.copy(r1)
    else:
        A1=A1+1
        r1=copy.copy(b)
        r2=list(reversed(b[A2:A1]))
        t=0
        for i in range(A1,A2):
            r1[i]=r2[t]
            t=t+1
        mutation=copy.copy(r1)
 
    returned_value=copy.copy(mutation)
    
    return returned_value
        
Time=0
T = 10000
Beta=1.05
Alpha=0.99
M0=5
BestS=copy.copy(tour)
currentS=copy.copy(tour)
currentCost=tourtodistance(currentS,vehicle)
BestCost=tourtodistance(BestS,vehicle)
w=0
while True :
    M=M0
    print "This Iteration number : " , w
    while True :
        rand1=numpy.random.rand()
        NewS=SAgetN(currentS)
        NewCost=tourtodistance(NewS,vehicle)
        Dcost = NewCost-currentCost
        form_1 = 1 / (numpy.exp((Dcost) / T))
        if Dcost < 0:
            currentS=copy.copy(NewS)
            currentCost=tourtodistance(currentS,vehicle)
            if NewCost < BestCost :
                BestS=copy.copy(NewS)
                BestCost=tourtodistance(BestS,vehicle)
        elif rand1 < form_1 :
            currentS=copy.copy(NewS)
            currentCost=tourtodistance(currentS,vehicle)
        M=M-1
        if M < 0 : 
            break
    Time = Time + M0
    T = Alpha*T
    M0 = Beta*M0
    w=w+1
    end_time = (time.time()-start_time) /60
    if T < 0.001 and end_time > 15:
        break
print "The T0 is : ", T
bestslice = subtourslice(BestS , vehicle)[0]
bestsubtour = subtour(bestslice,BestS
                      )
bestD=allvehicledistance(bestsubtour)
print(bestD)
combinesubtour = numpy.concatenate([x+[(len(nodes)-1)] for x in bestsubtour])
combinesubtour = numpy.append([(len(nodes)-1)],combinesubtour)
plt.plot([nodes[combinesubtour[i]][0] for i in range(len(combinesubtour))],[nodes[combinesubtour[i]][1] for i in range(len(combinesubtour))],'xb-')
for i in range(len(combinesubtour)):
    plt.annotate(combinesubtour[i],xy=(nodes[combinesubtour[i]][0],nodes[combinesubtour[i]][1] ))
plt.show

        
    
    

