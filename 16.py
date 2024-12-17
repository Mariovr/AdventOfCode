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
import sys
sys.setrecursionlimit(99999999)
from collections import Counter, defaultdict, deque
from aoc import AOC

aoc = AOC(16 , 2024)
input = aoc.input.strip().split('\n')
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
""" #11048 for part 1, 64 tiles part of best paths for part 2
#input = [line for line in stringlist.strip().split('\n')]
print(input)

#Brute force but only works for the example problem :(
def move(pos ,oor, mp, xdim , ydim, ec, seen, cost):
    #min cost to reach a square
    stepl = [ [0, 1],  [1, 0],  [0, -1],  [-1, 0]]
    npos = (0,0)
    costs = []
    for i, step in enumerate(stepl):
        npos = (pos[0] + step[0],pos[1] + step[1])
        if 0 <= npos[0] < xdim and 0 <= npos[1] < ydim and mp[(npos[0],npos[1])] == '.' and npos not in seen:
            seen.append(npos)
            oorc = abs(oor - i)
            if oorc  == 3:
                oorc = 1
            costd = 1 + 1000 * oorc
            if npos  == ec:
                print('reached end')
                print(cost+costd)
                return cost + costd
            else:
                ncost = move(npos , i, mp, xdim,ydim,ec,  seen[:],cost + costd)
            costs.append(ncost)
        else:
            costs.append(1e9)
    mc = min(costs)
    return mc

def parts():
    dimx = len(input)
    dimy = len(input[0])
    mp = {}
    sc, ec =(0,0) , (0,0)
    for i, line in enumerate(input):
        for  j, l in enumerate(list(line)):
            mp[(i,j)] = l
            if l == 'S':
                sc = (i,j)
                mp[(i,j)] = '.'
            if l =='E':
                ec = (i,j)
                mp[(i,j)] = '.'
    #cost = move(sc , oor, mp ,dimx , dimy, ec, seen , cost) #brute force solution for part1, but only works for example problem
    print('dims:' , dimx ,dimy)
    print('s' , sc)
    print('e' , ec)
    d = deque([])
    d.append((sc, 0 , 0)) #start c , oorientation, cost
    seen = set((sc,0))
    costm = {} #contains all visited positions + current orientation, with their lowest cost and history of steps to get there.
    costm[(sc,0)] = (0 , [sc])
    otlist = set()
    stepd = [ [0, 1],  [1, 0],  [0, -1],  [-1, 0]] #orientation is linked to step: 0, 1,2,3
    res = 1e9
    while(d):
        sc, oor, cost = d.pop()
        rl = []
        for i, step in enumerate(stepd):
            npos = (sc[0] + step[0],sc[1] + step[1])
            if 0 <= npos[0] < dimx and 0 <= npos[1] < dimy and mp[(npos[0],npos[1])] == '.': 
                oorc = abs(oor - i) #calc change in orientation
                if oorc  == 3:
                    oorc = 1
                costd = 1 + 1000 * oorc
                ncost = cost + costd
                if (npos,i) not in seen:
                    rl.append((npos,i , ncost))
                    seen.add((npos,i))
                    costm[(npos,i)] = (ncost, costm[(sc,oor)][1] + [npos])
                elif ncost <= costm[(npos,i)][0]:
                    rl.append((npos,i , ncost))
                    costm[(npos,i)] = (ncost, costm[(sc,oor)][1] + [npos])
                if npos  == ec:
                    if ncost <= res:
                        if ncost < res:
                            otlist = set()
                        res = ncost
                        for o in costm[(npos,i)][1]:
                            otlist.add(o)
                    print(len(otlist))
                    print('res: ' , res)
        rl.sort(key =lambda x : x[2], reverse = True )
        for r in rl:
            d.append((r[0] , r[1], r[2]))
    return res, len(otlist)

result1 , result2 = parts()
# Submit
print('Result 1:', result1)
#aoc.submit(1, result1)
print('Result 2:', result2)
#aoc.submit(2, result2)

