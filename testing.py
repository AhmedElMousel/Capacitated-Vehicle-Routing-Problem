# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 21:33:45 2020

@author: ElMousel
"""

import functools , operator , pandas , math , random , numpy , copy , matplotlib.pyplot as plt
import time
xls =pandas.ExcelFile('F:\Data\datafile2.xlsx')
sheet1 = pandas.read_excel(xls,'Sheet1')
sheet2 = pandas.read_excel(xls,'Sheet2')
nodes = sheet1.as_matrix()
depot = nodes[len(nodes)-1]
cities = nodes[:len(nodes)-1]
vehicle = sheet2.as_matrix()
tour = [44, 21, 34, 26, 40, 29, 43, 10, 19, 9, 38, 18, 12, 49, 16, 30, 31, 24, 0, 22, 46, 5, 28, 8, 37, 48, 4, 35, 2, 25, 36, 17, 47, 27, 6, 39, 23, 13, 32, 11, 3, 41, 1, 14, 45, 33, 20, 42, 15, 7]
newTour=[]
n=len(cities)
Mi = 200
current_time = time.time()
numpy.seterr(divide="ignore")

def intialsol(t):
    capacityused = numpy.zeros(len(vehicle))
    ttemp=copy.copy(t)
    sub=list()
    x=0
    while len(ttemp)!=0 and x<=len(vehicle)-1:
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
s=intialsol(tour)

