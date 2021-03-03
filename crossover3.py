# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 13:36:38 2020

@author: ElMousel
"""
import numpy as np
import random
import functools


parent1 = random.sample(range(9),9)
print "The parent1 is : ", parent1
parent2 = random.sample(range(9),9)
while functools.reduce(lambda i, j : i and j, map(lambda m, k: m == k, parent1, parent2), True) :
    parent2 = random.sample(range(9),9)
print "The parent2 is : ", parent2
crosspoint1 = np.random.randint(0,len(parent1)-2)
crosspoint2 = np.random.randint(crosspoint1+1,len(parent1)-1)
print "The crosspoints are : ", (crosspoint1,crosspoint2)

partialchild1_1 = parent2[crosspoint1:crosspoint2]
partialchild2_1 = parent1[crosspoint1:crosspoint2]
print "Pchild1 is", partialchild1_1 
print "Pchild2 is", partialchild2_1

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
print "child1 is : ", child1


            
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
print "child2 is : ", child2



