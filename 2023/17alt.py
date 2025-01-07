# This program is free software. It comes without any warranty, to the extent
# permitted by applicable law. You may use it, redistribute it and/or modify
# it, in whole or in part, provided that you do so at your own risk and do not
# hold the developers or copyright holders liable for any claim, damages, or
# other liabilities arising in connection with the software.
# 
#Developed by Mario Van Raemdonck, 2024;
#
# -*- coding: utf-8 -*-
#! /usr/bin/env python 
from collections import Counter, defaultdict, deque #defaultdict provides default function when accessing key not present
import heapq #heapify(list) , heappush(heap,item) , heappop(heap, item) returns lowest and removes, merge, nlargest(n, iterable, key=None), nsmallest
from aoc import AOC

aoc = AOC(17, 2023)
inpa = aoc.input.strip().split('\n')
stringlist ="""2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""
#inpa = [line.strip() for line in stringlist.strip().split('\n')]
X, Y = len(inpa), len(inpa[0])
steps = [[0, 1], [1, 0], [0, -1], [-1, 0]]
print(inpa)

def adjs(cur, mp , smin = 4 , smax = 10):
    for i in range(-1,2,1): 
        nx = cur[0][0] + steps[(cur[1]+i)%4][0] 
        ny = cur[0][1] + steps[(cur[1]+i)%4][1] 
        nstep = cur[2] + 1
        if 0<= nx < X and 0 <= ny <Y:
            nc = mp[(nx,ny)]
            if i == 0 and nstep <= smax:
                yield (nc, (( nx,ny) ,cur[1],nstep ) )
            elif i != 0 and nstep > smin:
                yield (nc,( (nx,ny) ,(cur[1]+i)%4, 1))


def dijkstra(start , target, mp, smin = 4 , smax = 10):
    pq= []
    heapq.heappush(pq, (0, (start, 0, 0) ) )
    heapq.heappush(pq, (0, (start, 1, 0) ) )
    dists = defaultdict(lambda : float("inf") )
    while len(pq) > 0:
        dist , cur = heapq.heappop(pq)
        if cur[0] == target and cur[2] >= smin:
            break
        for d , adj in adjs(cur, mp, smin , smax):
            if dist + d < dists[adj]:
                dists[adj] = d+ dist
                heapq.heappush(pq, (dist + d ,adj) )
    return dist

def parts():
    res = 0
    print('dims(x,y):' , X ,Y)
    mp = {}
    plist = []
    for i, line in enumerate(inpa):
        for  j, l in enumerate(list(line)):
            mp[(i,j)] = int(l)
            res += 1
    sc = (0,0)
    ec = (X-1 , Y-1)
    res1 = dijkstra(sc, ec, mp,0,3) #no minimum steps, 3 max
    res2 = dijkstra(sc, ec, mp,4,10) #4 minimum steps, 10 max
    return res1, res2

result1,result2 = parts()
# Submit
print('Result 1:', result1)
print('Result 2:', result2)
