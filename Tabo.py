# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 15:17:20 2020

@author: ElMousel
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 16:27:49 2020

@author: ElMousel
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 20:25:53 2020

@author: ElMousel
"""

import functools , operator , os , pandas , math , random , numpy , copy , matplotlib.pyplot as plt , itertools as itr

xls =pandas.ExcelFile('F:\Data\datafile.xlsx')
sheet1 = pandas.read_excel(xls,'Sheet1')
sheet2 = pandas.read_excel(xls,'Sheet2')
nodes = sheet1.as_matrix()
depot = nodes[len(nodes)-1]
cities = nodes[:len(nodes)-1]
vehicle = sheet2.as_matrix()
n=len(cities)
Mi = 2000
z=0
tour= random.sample(range(len(cities)),len(cities))
bestCandidate = tour
bestN = tour
numpy.seterr(divide="ignore")
P_Mutation = 0.2
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
def getTSN(t):
    itrList = list(itr.combinations(t, 2))
    Combinations = [[0 for x in range(len(t))] for y in range(len(itrList))]
    c=0
    for i in itrList:
        A1= itrList[c][0]
        A2 = itrList[c][1]
        w=0
        for i in t:
            if t[w]==A1:
                Combinations[c][w]=A2
            elif t[w]==A2:
                Combinations[c][w]=A1
            else:
                Combinations[c][w]=t[w]
            w=w+1
        c=c+1
    Sn=functools.reduce(numpy.append,(tourtodistance(x,vehicle) for x in Combinations))
    x=0
    for i in Sn:
        Combinations[x].append(Sn[x])
        x=x+1
    Cf = numpy.array(sorted(Combinations, key=lambda x: x[len(t)]))
    temp=copy.copy(Cf)
    temp=numpy.delete(Cf,len(t),axis=1)
    temp = temp.astype(int)
    
    return(temp)
def GA(b,bc):
    mutation=[]
    child1=[]
    child2=[]
    A1=numpy.random.randint(len(b))
    A2=numpy.random.randint(len(b))
    while A1== A2:
        A2=numpy.random.randint(len(b))
    if A1<A2 :
        A2=A2+1
        r1=copy.copy(b)
        r2=list(reversed(b[A1:A2]))
        r3=copy.copy(bc)
        r4=list(reversed(bc[A1:A2]))
        t=0
        for i in range(A1,A2):
            r1[i]=r2[t]
            r3[i]=r4[t]
            t=t+1
        child1=copy.copy(r1)
        child2=copy.copy(r3)
    else:
        A1=A1+1
        r1=copy.copy(b)
        r2=list(reversed(b[A2:A1]))
        r3=copy.copy(bc)
        r4=list(reversed(bc[A2:A1]))
        t=0
        for i in range(A1,A2):
            r1[i]=r2[t]
            r3[i]=r4[t]
            t=t+1
        child1=copy.copy(r1)
        child2=copy.copy(r3)
    if tourtodistance(child1,vehicle) > tourtodistance(child2,vehicle):
        mutation = copy.copy(child2)
    else:
        mutation = copy.copy(child1)
    rn1=numpy.random.randint(len(b))
    rn2=numpy.random.randint(len(b))
    rn3=numpy.random.randint(len(b))
    
    B1=mutation[rn1]
    B2=mutation[rn2]
    Xt=[]
    T_temp=copy.copy(mutation)
    w=0
    for i in T_temp:
        if T_temp[w]== B1:
            Xt=numpy.append(Xt,B2)
        elif T_temp[w]==B2:
            Xt=numpy.append(Xt,B1)
        else:
            Xt=numpy.append(Xt,T_temp[w])
        w=w+1
    mutation=Xt[:]
    
    Xt=[]
    B1=mutation[rn1]
    B2=mutation[rn3]
    w=0
    for i in T_temp:
        if mutation[w]== B1:
            Xt=numpy.append(Xt,B2)
        elif mutation[w]==B2:
            Xt=numpy.append(Xt,B1)
        else:
            Xt=numpy.append(Xt,mutation[w])
        w=w+1
 
    returned_value=copy.copy(Xt)
    returned_value = returned_value.astype(int)
    return returned_value
    
        
        
    

tabulist=[[]] 
lentabu=10
iteration=0
tabulist[0]=bestCandidate
while z<=Mi :
    print " This is the %i iteration ",z
    sNeighborhood = getTSN(bestCandidate)
    bestCandidate = sNeighborhood[0]
    
    for sCandidate in sNeighborhood:
        sCD=tourtodistance(sCandidate,vehicle)
        sBD=tourtodistance(bestCandidate,vehicle)
        r= any(numpy.array_equal(x, sCandidate) for x in tabulist)
        if not r :
            if sCD < sBD:
                bestCandidate=copy.copy(sCandidate)
                break
    sBD=tourtodistance(bestCandidate,vehicle)
    sBB=tourtodistance(bestN,vehicle)
    if sBD < sBB:
        bestN=copy.copy(bestCandidate)    
    tabulist=numpy.vstack([tabulist,bestCandidate])
    if len(tabulist) >= lentabu:
        tabulist=numpy.delete(tabulist,0,axis=0)
    if z%20==0 :
        lentabu = numpy.random.randint(10,20)
    if z%30==0 :
        if sBD < sBB :
            bestN = copy.copy(bestCandidate)
    Random_1=numpy.random.rand()
    if Random_1 <= P_Mutation:
        bestCandidate=GA(bestN,bestCandidate)
    if z%40 ==0 :
        Ran_1 = numpy.random.randint(1, len(cities) ) 
        Ran_2 = numpy.random.randint(1, len(cities) )
        bestCandidate[Ran_1],bestCandidate[Ran_2]=bestCandidate[Ran_2],bestCandidate[Ran_1]
        Ran_1 = numpy.random.randint(1, len(cities) )
        bestCandidate[Ran_1],bestCandidate[Ran_2]=bestCandidate[Ran_2],bestCandidate[Ran_1]
        Ran_3 = numpy.random.randint(1, len(cities) ) 
        Ran_4 = numpy.random.randint(1, len(cities) )
        bestCandidate[Ran_3],bestCandidate[Ran_4]=bestCandidate[Ran_4],bestCandidate[Ran_3]
        Ran_3 = numpy.random.randint(1, len(cities) )
        bestCandidate[Ran_3],bestCandidate[Ran_4]=bestCandidate[Ran_4],bestCandidate[Ran_3]
    if z%10==0 :
        bestslice = subtourslice(bestN , vehicle)[0]
        bestsubtour = subtour(bestslice,bestN)
        bestD=allvehicledistance(bestsubtour)
        print(bestD)
    
    z=z+1
        
bestN=list(bestN)      
bestslice = subtourslice(bestN , vehicle)[0]
bestsubtour = subtour(bestslice,bestN)
bestD=allvehicledistance(bestsubtour)
print(bestD)
combinesubtour = numpy.concatenate([x+[(len(nodes)-1)] for x in bestsubtour])
combinesubtour = numpy.append([(len(nodes)-1)],combinesubtour)
plt.plot([nodes[combinesubtour[i]][0] for i in range(len(combinesubtour))],[nodes[combinesubtour[i]][1] for i in range(len(combinesubtour))],'xb-')
for i in range(len(combinesubtour)):
    plt.annotate(combinesubtour[i],xy=(nodes[combinesubtour[i]][0],nodes[combinesubtour[i]][1] ))
plt.show
        

  