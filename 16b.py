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
from collections import defaultdict, deque
import heapq #heapify(list) , heappush(heap,item) , heappop(heap, item) returns lowest and removes, merge, nlargest(n, iterable, key=None), nsmallest
from aoc import AOC

aoc = AOC(16 , 2024)
inpa = aoc.input.strip().split('\n')
stringlist ="""#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
"""
#inpa = [line.strip() for line in stringlist.strip().split('\n')]
print(inpa)

steps = [[0, 1], [1, 0], [0, -1], [-1, 0]]

def adjs(poso):
    adjs = [ (1 , (poso[0] + steps[poso[2]][0] , poso[1] + steps[poso[2]][1] , poso[2]) ) ]
    adjs.append(  (1000 , (poso[0]  , poso[1]  , (poso[2]+ 1 ) % 4) ))
    adjs.append(  (1000 , (poso[0]  , poso[1]  , (poso[2] - 1 ) % 4) ))
    return adjs

def dijkstra(start , end, soor, toor, dimx, dimy, grid):
    pq= []
    heapq.heappush(pq, (0, (start[0] ,start[1] , soor )) )
    dists = defaultdict(lambda : float("inf") )
    dist = 0
    _from = defaultdict(set)
    while len(pq) > 0:
        dist , cur = heapq.heappop(pq)
        if (cur[0] , cur[1]) == end and (cur[2] == toor or toor is None):
            continue #break if only interested in part 1
        for d , adj in adjs(cur):
            if dist + d < dists[adj] and 0<= adj[0] < dimx and 0 <= adj[1] < dimy and grid[(adj[0],adj[1])] == '.':
                dists[adj] = d+ dist
                heapq.heappush(pq, (dist + d , adj) )
                _from[adj] = set([cur])
            elif dist + d <= dists[adj] and 0<= adj[0] < dimx and 0 <= adj[1] < dimy and grid[(adj[0],adj[1])] == '.':
                _from[adj].add(cur)
    mindist = min([dists[(end[0] , end[1] , i ) ] for i in range(4) ])
    return mindist, _from, [ state for state in dists.keys() if state[0] == end[0] and state[1] == end[1] and dists[state] == mindist]

def parts():
    dimx, dimy = len(inpa), len(inpa[0])
    print('dims(x,y):' , dimx ,dimy)
    mp = {}
    sc , ec= (0,0) , (0,0)
    for i, line in enumerate(inpa):
        for  j, l in enumerate(list(line)):
            mp[(i,j)] = l
            if l == 'S':
                mp[(i,j)] = '.'
                sc = (i,j)
            if l == 'E':
                mp[(i,j)] = '.'
                ec = (i,j)
    print('start: ' , sc , 'end: ' , ec)
    res1, _from, minends = dijkstra(sc, ec, 0,None, dimx, dimy, mp)
    print('min end nodes: ' , minends )
    stack = deque(minends )
    goodnode = set()
    while(stack):
        test = stack.popleft()
        goodnode.add(test)
        for node in _from[test]:
            if node not in goodnode:
                stack.append(node)
    return res1 , len(set([(gn[0] , gn[1] ) for gn in goodnode ] )) #convert goodnodes that contain oorientation info to pure unique positions to identify tiles part of best path 

result1,result2 = parts()
print('Result 1:', result1)
print('Result 2:', result2)
