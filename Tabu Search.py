# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 16:35:37 2020

@author: ElMousel
"""

import functools, operator, os, pandas, math, random, numpy, copy, matplotlib.pyplot as plt

xls = pandas.ExcelFile('F:\Data\datafile.xlsx')
sheet1 = pandas.read_excel(xls, 'Sheet1')
sheet2 = pandas.read_excel(xls, 'Sheet2')
nodes = sheet1.as_matrix()
depot = nodes[len(nodes) - 1]
cities = nodes[:len(nodes) - 1]
vehicle = sheet2.as_matrix()
tour = random.sample(range(len(cities)), len(cities))
newTour = []
n = len(cities)
T0 = 1000000
Mi = 100000

Alpha = 0.8
numpy.seterr(divide="ignore")


def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def totaldistancetour(tour):
    d = 0
    for i in range(1, len(tour)):
        x1 = cities[tour[i - 1]][0]
        y1 = cities[tour[i - 1]][1]
        x2 = cities[tour[i]][0]
        y2 = cities[tour[i]][1]
        d = d + distance(x1, y1, x2, y2)
    x1 = cities[tour[len(tour) - 1]][0]
    y1 = cities[tour[len(tour) - 1]][1]
    x2 = depot[0]
    y2 = depot[1]
    d = d + distance(x1, y1, x2, y2)
    x1 = cities[tour[0]][0]
    y1 = cities[tour[0]][1]
    x2 = depot[0]
    y2 = depot[1]
    d = d + distance(x1, y1, x2, y2)
    return d


def subtourslice(tour, vehicle):
    capacityused = numpy.zeros(len(vehicle))
    k = 0
    slice = []
    mass = []
    for i in range(len(vehicle)):

        while capacityused[i] <= vehicle[i][1] and k <= (len(tour) - 1):
            capacityused[i] = capacityused[i] + cities[tour[k]][2]
            if capacityused[i] > vehicle[i][1]:
                capacityused[i] = capacityused[i] - cities[tour[k]][2]
                k = k - 1
                slice.append(k)
                k = k + 1
                break
            k = k + 1
        mass.append(capacityused[i])
    slice.append(k - 1)
    return slice, mass


def subtour(slice, tour):
    sub = []
    sub.append(tour[:(slice[0] + 1)])
    for i in range(0, len(slice) - 1):
        sub.append(tour[(slice[i] + 1):(slice[i + 1] + 1)])
    return sub


def allvehicledistance(sub):
    alldistance = functools.reduce(operator.add, (totaldistancetour(x) for x in sub), 0)
    return alldistance


def tourtodistance(tour, vehicle):
    u = subtourslice(tour, vehicle)
    v = subtour(u[0], tour)
    total = allvehicledistance(v)
    return total


def SAgetN(tourr):
    u = subtourslice(tourr, vehicle)[0]
    v = subtour(u, tourr)
    i = numpy.random.randint(0, len(v))
    ii = numpy.random.randint(0, len(v))
    while ii == i:
        ii = numpy.random.randint(0, len(v))
    j = numpy.random.randint(0, len(v[i]))
    jj = numpy.random.randint(0, len(v[ii]))
    A1 = v[i][j]
    A2 = v[ii][jj]
    tempTour = []
    w = 0
    for i in tourr:
        if tourr[w] == A1:
            tempTour.append(A2)
        elif tourr[w] == A2:
            tempTour.append(A1)
        else:
            tempTour.append(tour[w])
        w = w + 1
    tempTour = list(tempTour)
    return tempTour


for i in range(Mi):

    oldDistance = tourtodistance(tour, vehicle)
    newTour = SAgetN(tour)
    newDistance = tourtodistance(newTour, vehicle)
    form_1 = 1 / (numpy.exp((newDistance - oldDistance) / T0))
    rand1 = numpy.random.rand()
    if rand1 <= form_1:
        tour = copy.copy(newTour)
        if newDistance < oldDistance:
            T0 = Alpha * T0

print "The T0 is : ", T0
bestslice = subtourslice(tour, vehicle)[0]
bestsubtour = subtour(bestslice, tour)
bestD = allvehicledistance(bestsubtour)
print(bestD)
combinesubtour = numpy.concatenate([x + [(len(nodes) - 1)] for x in bestsubtour])
combinesubtour = numpy.append([(len(nodes) - 1)], combinesubtour)
plt.plot([nodes[combinesubtour[i]][0] for i in range(len(combinesubtour))],
         [nodes[combinesubtour[i]][1] for i in range(len(combinesubtour))], 'xb-')
for i in range(len(combinesubtour)):
    plt.annotate(combinesubtour[i], xy=(nodes[combinesubtour[i]][0], nodes[combinesubtour[i]][1]))
plt.show



