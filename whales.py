# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 13:30:53 2020

@author: ElMousel
"""

import functools , operator , pandas , math , random  , copy , matplotlib.pyplot as plt , itertools as itr
import  numpy as np ,  time 
current_time = time.time()
xls =pandas.ExcelFile('F:\Data\datafile.xlsx')
sheet1 = pandas.read_excel(xls,'Sheet1')
sheet2 = pandas.read_excel(xls,'Sheet2')
nodes = sheet1.as_matrix()
depot = nodes[len(nodes)-1]
cities = nodes[:len(nodes)-1]
vehicle = sheet2.as_matrix()
n=len(cities)
itrr = 1000
P_Mutation = 0.5
b = np.random.randint(0,n)
tour= random.sample(range(len(cities)),len(cities))
min_distance=[]
temp_plot=[]
np.seterr(divide="ignore")
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
#def subtourslice(t , vehicle):
#    capacityused = np.zeros(len(vehicle))
#    k = 0
#    slice=[]
#    mass=[]
#    x=0
#    for i in range(len(vehicle)):
#       
#        while capacityused[x] <= vehicle[x][1] and k <= (len(t)-1):
#            capacityused[x]=capacityused[x]+cities[t[k]][2]
#            if capacityused[x] > vehicle[x][1]:
#                capacityused[x]=capacityused[x]-cities[t[k]][2]
#                k = k-1
#                slice.append(k)
#                k = k+1
#                break
#            k=k+1
#        mass.append(capacityused[x])
#        x=x+1
#    slice.append(k-1)
#    return slice,mass
#def subtour(slice,t):
#    sub=[]
#    sub.append(t[:(slice[0]+1)])
#    for i in range (0,len(slice)-1):
#        sub.append(t[(slice[i]+1):(slice[i+1]+1)])
#    return sub
def intialsol(t):
    capacityused = np.zeros(len(vehicle))
    ttemp=list(t)
    sub=list()
    x=0
    while len(ttemp)!=0 and x<=len(vehicle):
        w=0
        path=[]
        while len(ttemp)!=0 and w <= (len(ttemp)-1):
            c=capacityused[x]+cities[ttemp[w]][2]
            if c <= vehicle[x][1] :
                capacityused[x]=c
                path.append(ttemp[w])
                ttemp.remove(ttemp[w])
            else:
                w=w+1
        sub.append(path)
        x=x+1
    return sub
def allvehicledistance(sub):
    alldistance = functools.reduce(operator.add,(totaldistancetour(x) for x in sub) , 0)
    return alldistance
def tourtodistance(t,vehicle):
#    u=subtourslice(t,vehicle)
#    v=subtour(u[0],t)
    v=intialsol(t)
    total=allvehicledistance(v)
    return total
print "The intial distance is : ",tourtodistance(tour,vehicle)
def twopoint_crossover(parent1,parent2):
    parent1 = list(parent1)
    parent2 = list(parent2)
    crosspoint1 = np.random.randint(0,len(parent1)-2)
    crosspoint2 = np.random.randint(crosspoint1+1,len(parent1)-1)
    partialchild1_1 = parent2[crosspoint1:crosspoint2]
    partialchild2_1 = parent1[crosspoint1:crosspoint2]
    
    partialchild1_2 = []
    partialchild2_2 = []

    partialchild1_3 = []
    partialchild2_3 = []
    for i in range(0,crosspoint1):
        if parent1[i] in partialchild1_1 :
            partialchild1_2.append(-1)
        else :
            partialchild1_2.append(parent1[i])
        
    for i in range(crosspoint2 , len(parent1)):
        if parent1[i] in partialchild1_1 :
            partialchild1_3.append(-1)
        else :
            partialchild1_3.append(parent1[i])
    child1 =  partialchild1_2[:] + partialchild1_1[:] + partialchild1_3[:]
    tempchild1 = np.array(child1)
    empty = [int(i) for i in ((np.where(tempchild1==-1))[0].tolist())]
    
    w=0
    while w < len(empty):
        for i in range(crosspoint2  , len(parent1)):
            if not (parent2[i] in child1):
                child1[empty[w]]= parent2[i]
                w=w+1
        for i in range(0 , crosspoint1):
            if not (parent2[i] in child1):
                child1[empty[w]]= parent2[i]
                w=w+1
    
            
    for i in range(0,crosspoint1):
        if parent2[i] in partialchild2_1 :
            partialchild2_2.append(-1)
        else :
            partialchild2_2.append(parent2[i])

    for i in range(crosspoint2 , len(parent1)):
        if parent2[i] in partialchild2_1 :
            partialchild2_3.append(-1)
        else :
            partialchild2_3.append(parent2[i])
    child2 =  partialchild2_2[:] + partialchild2_1[:] + partialchild2_3[:]
    tempchild2 = np.array(child2)
    empty2 = [int(i) for i in ((np.where(tempchild2==-1))[0].tolist())]
    w=0
    while w < len(empty2):
        for i in range(crosspoint2  , len(parent1)):
            if not (parent1[i] in child2):
                child2[empty2[w]]= parent1[i]
                w=w+1
        for i in range(0 , crosspoint1):
            if not (parent1[i] in child2):
                child2[empty2[w]]= parent1[i]
                w=w+1
    if tourtodistance(child1,vehicle) <= tourtodistance(child2,vehicle):
        return child1
    else:
        return child2
def partialmapped_crossover(parent1,parent2):
    mutation=[]
    firstCrossPoint = np.random.randint(0,len(parent1)-2)
    secondCrossPoint = np.random.randint(firstCrossPoint+1,len(parent1)-1)
    
    parent1MiddleCross = parent1[firstCrossPoint:secondCrossPoint]
    parent2MiddleCross = parent2[firstCrossPoint:secondCrossPoint]
    
    temp_child1 = list(parent1[:firstCrossPoint]) + list(parent2MiddleCross) + list(parent1[secondCrossPoint:])
    temp_child2 = list(parent2[:firstCrossPoint]) + list(parent1MiddleCross) + list(parent2[secondCrossPoint:])
    
    relations = []
    for i in range(len(parent1MiddleCross)):
        relations.append([parent2MiddleCross[i], parent1MiddleCross[i]])
    child1=recursion1(temp_child1,firstCrossPoint,secondCrossPoint,parent1MiddleCross,parent2MiddleCross,relations)
    child2=recursion2(temp_child2,firstCrossPoint,secondCrossPoint,parent1MiddleCross,parent2MiddleCross,relations)
    if tourtodistance(child1,vehicle) > tourtodistance(child2,vehicle):
        mutation = copy.copy(child2)
    else:
        mutation = copy.copy(child1)
    rn1=np.random.randint(len(parent1))
    rn2=np.random.randint(len(parent1))
    rn3=np.random.randint(len(parent1))
    
    B1=mutation[rn1]
    B2=mutation[rn2]
    Xt=[]
    T_temp=copy.copy(mutation)
    w=0
    for i in T_temp:
        if T_temp[w]== B1:
            Xt=np.append(Xt,B2)
        elif T_temp[w]==B2:
            Xt=np.append(Xt,B1)
        else:
            Xt=np.append(Xt,T_temp[w])
        w=w+1
    mutation=Xt[:]
    
    Xt=[]
    B1=mutation[rn1]
    B2=mutation[rn3]
    w=0
    for i in T_temp:
        if mutation[w]== B1:
            Xt=np.append(Xt,B2)
        elif mutation[w]==B2:
            Xt=np.append(Xt,B1)
        else:
            Xt=np.append(Xt,mutation[w])
        w=w+1
    returned_value=copy.copy(Xt)
    returned_value = returned_value.astype(int)
    return returned_value
def recursion1 (temp_child , firstCrossPoint , secondCrossPoint , parent1MiddleCross , parent2MiddleCross,relations) :
    child = np.array([0 for i in range(len(tour))])
    for i,j in enumerate(temp_child[:firstCrossPoint]):
        c=0
        for x in relations:
            if j == x[0]:
                child[i]=x[1]
                c=1
                break
        if c==0:
            child[i]=j
    j=0
    for i in range(firstCrossPoint,secondCrossPoint):
        child[i]=parent2MiddleCross[j]
        j+=1

    for i,j in enumerate(temp_child[secondCrossPoint:]):
        c=0
        for x in relations:
            if j == x[0]:
                child[i+secondCrossPoint]=x[1]
                c=1
                break
        if c==0:
            child[i+secondCrossPoint]=j
    child_unique=np.unique(child)
    if len(child)>len(child_unique):
        child=recursion1(child,firstCrossPoint,secondCrossPoint,parent1MiddleCross,parent2MiddleCross,relations)
    return(child)
def recursion2(temp_child,firstCrossPoint,secondCrossPoint,parent1MiddleCross,parent2MiddleCross,relations):
    child = np.array([0 for i in range(len(tour))])
    for i,j in enumerate(temp_child[:firstCrossPoint]):
        c=0
        for x in relations:
            if j == x[1]:
                child[i]=x[0]
                c=1
                break
        if c==0:
            child[i]=j
    j=0
    for i in range(firstCrossPoint,secondCrossPoint):
        child[i]=parent1MiddleCross[j]
        j+=1

    for i,j in enumerate(temp_child[secondCrossPoint:]):
        c=0
        for x in relations:
            if j == x[1]:
                child[i+secondCrossPoint]=x[0]
                c=1
                break
        if c==0:
            child[i+secondCrossPoint]=j
    child_unique=np.unique(child)
    if len(child)>len(child_unique):
        child=recursion2(child,firstCrossPoint,secondCrossPoint,parent1MiddleCross,parent2MiddleCross,relations)
    return(child)
def ordered_crossover(parent1,parent2):
    parent1=list(parent1)
    parent2=list(parent2)
    crosspoint1 = np.random.randint(0,len(parent1)-2)
    crosspoint2 = np.random.randint(crosspoint1+1,len(parent1)-1)
    partialchild1_1 = parent2[crosspoint1:crosspoint2]
    partialchild2_1 = parent1[crosspoint1:crosspoint2]
    
    partialchild1_2 = []
    partialchild2_2 = []

    partialchild1_3 = []
    partialchild2_3 = []
    w = len(parent1)-1
    c = len(parent1)-1
    while w >= crosspoint2:
        while c >= 0:
            if not(parent2[c] in partialchild1_1):
                partialchild1_2.append(parent2[c])
                c=c-1
                w=w-1
                break
            else:
                c=c-1

    w = crosspoint1-1
    while w >= 0 :
        while c >= 0:
            if not(parent2[c] in partialchild1_1):
                partialchild1_3.append(parent2[c])
                c=c-1
                w=w-1
                break
            else:
                c=c-1
            
    child1= list(reversed(partialchild1_3[:])) + partialchild1_1[:] + list(reversed(partialchild1_2[:]))
    w = len(parent1)-1
    c = len(parent1)-1

    while w >= crosspoint2:
        while c >= 0:
            if not(parent1[c] in partialchild2_1):
                partialchild2_2.append(parent1[c])
                c=c-1
                w=w-1
                break
            else:
                c=c-1
    w = crosspoint1-1
    while w >= 0 :
        while c >= 0:
            if not(parent1[c] in partialchild2_1):
                partialchild2_3.append(parent1[c])
                c=c-1
                w=w-1
                break
            else:
                c=c-1
            
    child2= list(reversed(partialchild2_3[:])) + partialchild2_1[:] + list(reversed(partialchild2_2[:]))
    if tourtodistance(child1,vehicle) <= tourtodistance(child2,vehicle):
        return child1
    else:
        return child2
def intial_popultion():
    t1 = random.sample(range(len(cities)),len(cities))
    whale=[[]]
    whale[0]=t1
    whale_size=10
    for i in range(whale_size-1):
        t = random.sample(range(len(cities)),len(cities))
        while any(np.array_equal(x, t) for x in whale) :
            t = random.sample(range(len(cities)),len(cities))
        whale=np.vstack([whale,t])
    return whale
def ordered_whale(whale):
    wa=copy.copy(whale)
    Sn=functools.reduce(np.append,(tourtodistance(x,vehicle) for x in wa))
    temp=sorted(Sn)
    index=np.where(Sn==temp[0])
    bestt=wa[index[0][0]]
    return bestt
def swapping(bb):
    i = np.random.randint(0,n)
    j = np.random.randint(0,n)
    tem=copy.copy(bb)
    while i == j :
      j = np.random.randint(0,n)
    tem[i],tem[j]=tem[j],tem[i]
    return tem
def K_WOA(kk,bb):
    b_best=copy.copy(bb)
    w=0
    taboo = []
    taboo.append(tourtodistance(b_best,vehicle))
    while w <= kk :
        temp = copy.copy(bb) 
        temp = swapping(temp)
        d_t = tourtodistance(temp,vehicle)
        if d_t in taboo[:] :
            w = w - 1
        else :
            d_b = tourtodistance(b_best,vehicle)
            if d_t <= d_b:
                b_best = copy.copy(temp)
            taboo.append(d_t)
        w = w + 1  
    return b_best
def GA(b):
    mutation=[]
    A1=np.random.randint(len(b))
    A2=np.random.randint(len(b))
    while A1== A2:
        A2=np.random.randint(len(b))
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
    rn1=np.random.randint(len(b))
    rn2=np.random.randint(len(b))
    rn3=np.random.randint(len(b))
    B1=mutation[rn1]
    B2=mutation[rn2]
    Xt=[]
    T_temp=copy.copy(mutation)
    w=0
    for i in T_temp:
        if T_temp[w]== B1:
            Xt=np.append(Xt,B2)
        elif T_temp[w]==B2:
            Xt=np.append(Xt,B1)
        else:
            Xt=np.append(Xt,T_temp[w])
        w=w+1
    mutation=Xt[:]
    Xt=[]
    B1=mutation[rn1]
    B2=mutation[rn3]
    w=0
    for i in T_temp:
        if mutation[w]== B1:
            Xt=np.append(Xt,B2)
        elif mutation[w]==B2:
            Xt=np.append(Xt,B1)
        else:
            Xt=np.append(Xt,mutation[w])
        w=w+1
    returned_value=copy.copy(Xt)
    returned_value = returned_value.astype(int)
    return returned_value
def SAgetN(route):
     best = route
     Ran_1 = np.random.randint(1, len(cities) ) 
     Ran_2 = np.random.randint(1, len(cities) )
     best[Ran_1],best[Ran_2]=best[Ran_2],best[Ran_1]
     improved = True
     w=0
     while improved and w<=1:
          print improved
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

whale = intial_popultion()
wa = copy.copy(whale)
best = ordered_whale(wa)
best_over = ordered_whale(wa)
for i in range(itrr):
    print " iteration number : " , i
    z = 0
    temp_whale=copy.copy(wa)
    r_mutation = np.random.rand()
    for j in temp_whale :
        p = np.random.rand()
        pb = 1 - ((i/itrr)**2)
        ra = np.random.rand()
        if p < 0.5 :
            if ra > pb:
                temp_whale[z] = ordered_crossover(temp_whale[z],best)
            elif ra <= pb:
                x_random_index=np.random.randint(len(whale))
                x_random = wa[x_random_index]
                temp_whale[z] = partialmapped_crossover(x_random,best)
        elif p >= 0.5:
            temp_whale[z] = twopoint_crossover(temp_whale[z],best)
        z=z+1
#    z=0
#    r=np.random.rand()
#    C=2*r
#    a = 2 - (2* (i/itrr))
#    A = (2*a*r)- a
#    l=random.uniform(-1,1)
#    j=np.random.randint(0,n)
#    D = best[j]
#    cos=math.cos(2*(np.pi)*l)
#    euler=math.exp(b*l)
#    first= abs(j +((C*n)/A))
#    second = (D*euler*cos)+j
#    for s in temp_whale :
#        p = np.random.rand()
#        if p < 0.5 :
#            if A < 1:
#                k= abs( math.floor(second + (second/n) + 1))
#                if k > 100 :
#                    k = np.random.randint(100,150)
#                temp_whale[z] = K_WOA(k,temp_whale[z])
#            elif A >= 1:
#                x_random_index=np.random.randint(len(whale))
#                x_random = wa[x_random_index]
#                k= abs(math.floor(first + (first/n) + 1))
#                if k > 100 :
#                    k = np.random.randint(100,150)
#                temp_whale[z] = K_WOA(k,x_random)
#        elif p >= 0.5 :
#            k= abs(math.floor(first + (first/n) + 1))
#            if k > 100 :
#                k = np.random.randint(100,150)
#            temp_whale[z] = K_WOA(k,temp_whale[z])
#        z=z+1
    wa = copy.copy(temp_whale)
    best= ordered_whale(wa)
    
    if i%30 ==0 :
        Ran_1 = np.random.randint(1, len(cities) ) 
        Ran_2 = np.random.randint(1, len(cities) )
        best[Ran_1],best[Ran_2]=best[Ran_2],best[Ran_1]
        Ran_1 = np.random.randint(1, len(cities) )
        best[Ran_1],best[Ran_2]=best[Ran_2],best[Ran_1]
        Ran_3 = np.random.randint(1, len(cities) ) 
        Ran_4 = np.random.randint(1, len(cities) )
        best[Ran_3],best[Ran_4]=best[Ran_4],best[Ran_3]
        Ran_3 = np.random.randint(1, len(cities) )
        best[Ran_3],best[Ran_4]=best[Ran_4],best[Ran_3]
    if r_mutation <= P_Mutation :
        best = GA(best_over)
    if tourtodistance(best,vehicle) <= tourtodistance(best_over,vehicle):
        best_over=copy.copy(best)
    if i%10 ==0:
        print " D = " , tourtodistance(best_over,vehicle)
    temp_plot=np.append(temp_plot,i)
    min_distance=np.append(min_distance,tourtodistance(best,vehicle))
bestN=list(best_over)      
#bestslice = subtourslice(bestN , vehicle)[0]
#bestsubtour = subtour(bestslice,bestN)
bestsubtour=intialsol(bestN)
bestD=allvehicledistance(bestsubtour)
print(bestD)
combinesubtour = np.concatenate([x+[(len(nodes)-1)] for x in bestsubtour])
combinesubtour = np.append([(len(nodes)-1)],combinesubtour)
plt.subplot(2,1,1)
plt.plot([nodes[combinesubtour[i]][0] for i in range(len(combinesubtour))],[nodes[combinesubtour[i]][1] for i in range(len(combinesubtour))],'xb-')
for i in range(len(combinesubtour)):
    plt.annotate(combinesubtour[i],xy=(nodes[combinesubtour[i]][0],nodes[combinesubtour[i]][1] ))
plt.subplot(2,1,2)
plt.plot(temp_plot, min_distance)
plt.title("Distance vs. Iterations", fontsize=20, fontweight='bold')
plt.xlabel("Iterations", fontsize=18, fontweight='bold')
plt.ylabel("Distance", fontsize=18, fontweight='bold')
plt.xlim(0, 1000)
plt.xticks(np.arange(min(temp_plot), max(temp_plot), 200), fontweight='bold')
plt.yticks(fontweight='bold')
plt.show()
end_time = (time.time() - current_time)/60
print " The computatinal time is : " , end_time , "min"
            
            




    

    
    

        
       
    