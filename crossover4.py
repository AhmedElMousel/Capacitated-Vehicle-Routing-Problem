# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 16:09:20 2020

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

partialchild1_1 = parent1[crosspoint1:crosspoint2]
partialchild2_1 = parent2[crosspoint1:crosspoint2]
print "Pchild1 is", partialchild1_1 
print "Pchild2 is", partialchild2_1

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
print "Child1 is : ", child1

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
print "Child2 is : ", child2