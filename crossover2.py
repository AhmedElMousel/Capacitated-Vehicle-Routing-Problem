# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 12:42:18 2020

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
crosspoint=np.random.randint(0,len(parent1)-1)
print crosspoint
partialchild1_1 = parent1[:crosspoint]
print "Pchild1 is", partialchild1_1 
partialchild2_1 = parent2[:crosspoint]
print "Pchild2 is", partialchild2_1 
partialchild1_2 = []
partialchild2_2 = []
c = len(partialchild1_1)
temp_c=0
while c < len(parent1):
    while temp_c < len(parent1) :
        if not (parent2[temp_c] in partialchild1_1):
            partialchild1_2.append(parent2[temp_c])
            c=c+1
            temp_c=temp_c+1
            break
        else :
            temp_c=temp_c+1
child1=  partialchild1_1[:] +  partialchild1_2[:]
print "child1 is", child1

c = len(partialchild2_1)
temp_x=0

while c < len(parent2):
    while temp_x < len(parent1) :
        if not (parent1[temp_x] in partialchild2_1):
            partialchild2_2.append(parent1[temp_x])
            c=c+1
            temp_x=temp_x+1
            break
        else :
            temp_x=temp_x+1
child2=  partialchild2_1[:] +  partialchild2_2[:]
print "child2 is", child2


    

            
        