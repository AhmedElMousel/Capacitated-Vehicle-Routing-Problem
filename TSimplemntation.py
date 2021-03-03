# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 16:35:37 2020

@author: ElMousel
"""

import functools , operator , pandas , math , random , numpy , copy , matplotlib.pyplot as plt
import time
xls =pandas.ExcelFile('F:\Data\datafile.xlsx')
sheet1 = pandas.read_excel(xls,'Sheet1')
sheet2 = pandas.read_excel(xls,'Sheet2')
nodes = sheet1.as_matrix()
depot = nodes[len(nodes)-1]
cities = nodes[:len(nodes)-1]
vehicle = sheet2.as_matrix()
tour =random.sample(range(len(cities)),len(cities))
newTour=[]
temp_plot=[]
min_distance=[]
n=len(cities)
Mi = 10
current_time = time.time()
numpy.seterr(divide="ignore")
def distance(x1,y1,x2,y2):
    return math.sqrt((x1-x2)**2+(y1-y2)**2)
def dist(x,y):
    x1=cities[x][0]
    y1=cities[x][1]
    x2=cities[y][0]
    y2=cities[y][1]
    d=distance(x1,y1,x2,y2)
    return d
def intial():
    index=list(range(len(cities)))
    xd = depot[0]
    yd= depot[1]
    da=[]
    for i in range(len(cities)):
        da.append(distance(cities[i][0],cities[i][0],xd,yd))
    index.sort(key=lambda i: da[i])
    return index
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
def intialsol(t):
    capacityused = numpy.zeros(len(vehicle))
    ttemp=list(t)
    sub=list()
    q=0
    while len(ttemp)!=0 and q != len(vehicle)-1:
        w=0
        path=[]
        while len(ttemp)!=0 and w <= (len(ttemp)-1):
            c=capacityused[q]+cities[ttemp[w]][2]
            if c <= vehicle[q][1] :
                capacityused[q]=c
                path.append(ttemp[w])
                ttemp.remove(ttemp[w])
            else:
                w=w+1
        sub.append(path)
        q=q+1 
    return sub
def allvehicledistance(sub):
    alldistance = functools.reduce(operator.add,(totaldistancetour(x) for x in sub) , 0)
    return alldistance
def tourtodistance(t,vehicle):
    v=intialsol(t)
#    u=subtourslice(t,vehicle)
#    v=subtour(u[0],t)
    total=allvehicledistance(v)
    return total
#print "The intial distance is : ",tourtodistance(tour,vehicle)
def SAgetN(route):
     best = route
     Ran_1 = numpy.random.randint(1, len(cities) ) 
     Ran_2 = numpy.random.randint(1, len(cities) )
     best[Ran_1],best[Ran_2]=best[Ran_2],best[Ran_1]
     improved = True
     w=0
     while improved and w <= 5 :
          improved = False
          for i in range(1, len(route)-2):
               for j in range(i+1, len(route)):
                    if j-i == 1: continue # changes nothing, skip then
                    new_route = route[:]
                    new_route[i:j] = route[j-1:i-1:-1] # this is the 2woptSwap
                    x=tourtodistance(new_route,vehicle)
                    y=tourtodistance(best,vehicle)
                    if x <= y:  # what should cost be?
                         best = new_route
                         improved = True
          route = best
          w=w+1
     return best

def temperature(fraction):
    return max(0.0001, min(1, 1 - fraction))
def acceptance_probability(cost, new_cost, temperature):
    if new_cost < cost:
        # print("    - Acceptance probabilty = 1 as new_cost = {} < cost = {}...".format(new_cost, cost))
        return 1
    else:
        p = numpy.exp(- (new_cost - cost) / temperature)
        # print("    - Acceptance probabilty = {:.3g}...".format(p))
        return p
best=copy.copy(tour)
best_over=copy.copy(best)        
for i in range(Mi):
    print "no.itr", i
    fraction= i/float(Mi)
    T0 = temperature(fraction)
    oldDistance = tourtodistance(best,vehicle)
    newTour=SAgetN(best)
    newDistance = tourtodistance(newTour,vehicle)
    form_1 = acceptance_probability(oldDistance,newDistance,T0)
    rand1=numpy.random.rand()
    if rand1 <= form_1:
        best=copy.copy(newTour)
    if tourtodistance(best,vehicle) <= tourtodistance(best_over,vehicle):
        best_over=copy.copy(best)
    if i%10 ==0:
        print "The distance is : ",tourtodistance(best_over,vehicle)
    temp_plot=numpy.append(temp_plot,i)
    min_distance=numpy.append(min_distance,tourtodistance(best_over,vehicle))
    
print "The T0 is : ",T0
bestsubtour = intialsol(best_over)
#bestslice = subtourslice(best_over , vehicle)[0]
#bestsubtour = subtour(bestslice,best_over)
bestD=allvehicledistance(bestsubtour)
print(bestD)
combinesubtour = numpy.concatenate([x+[(len(nodes)-1)] for x in bestsubtour])
combinesubtour = numpy.append([(len(nodes)-1)],combinesubtour)
plot1 = plt.figure(1)
plt.plot([nodes[combinesubtour[i]][0] for i in range(len(combinesubtour))],[nodes[combinesubtour[i]][1] for i in range(len(combinesubtour))],'xb-')
for i in range(len(combinesubtour)):
    plt.annotate(combinesubtour[i],xy=(nodes[combinesubtour[i]][0],nodes[combinesubtour[i]][1] ))
plot2 = plt.figure(2)
plt.plot(temp_plot, min_distance)
plt.title("Distance vs. Iterations", fontsize=20, fontweight='bold')
plt.xlabel("Iterations", fontsize=18, fontweight='bold')
plt.ylabel("Distance", fontsize=18, fontweight='bold')
plt.xlim(0, 10)
plt.xticks(numpy.arange(min(temp_plot), max(temp_plot), 100), fontweight='bold')
plt.yticks(fontweight='bold')
plt.show()
end_time = (time.time() - current_time)/60
print " The computatinal time is : " , end_time , "min"
        
    
    