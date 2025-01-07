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
from aoc import AOC
from collections import Counter, defaultdict, deque #defaultdict provides default function when accessing key not present
import re
import heapq #heapify(list) , heappush(heap,item) , heappop(heap, item) returns lowest and removes, merge, nlargest(n, iterable, key=None), nsmallest

aoc = AOC(18 , 2024)
inpa = aoc.input.strip().split('\n')
stringlist ="""5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
"""
#inpa = [line for line in stringlist.strip().split('\n')]

steps = [[0, 1], [1, 0], [0, -1], [-1, 0]]
stepsa = [[1, 1], [-1, -1], [1, -1], [-1, 1]] + steps
nums = lambda s : [int(x) for x in re.findall(r'-?\d+', s)]

def print_map(dmap, dimx , dimy):
    mapl = [['.' for i in range(dimy)] for j in range(dimx)]
    for i in range(dimx):
        for j in range(dimy):
            mapl[i][j] = dmap[(i,j)]
    with open('map.txt','w') as f:
        for line in mapl:
            print(''.join(line) )
            f.write(''.join(line) + '\n')

def is_close(dmap , dimx, dimy):
    startl =[]
    for i in range(dimx):
        if dmap[(i,0)] == '#':
            startl.append((i,0))
    startr =[]
    for i in range(dimx):
        if dmap[(i,dimy-1)]== '#':
            startr.append((i,dimy-1))

    d = deque(startl)
    seen= set()
    #check wall from left to up
    while(d):
        sc = d.pop()
        seen.add(sc)
        for dx , dy in stepsa:
            nx = sc[0] + dx
            ny = sc[1] + dy
            if 0<= nx < dimx and 0<= ny < dimy and dmap[(nx,ny)] == '#' and (nx,ny) not in seen:
                d.append((nx,ny))
                if nx ==0:
                    return True
    d = deque(startr)
    seen= set()
    #check wall from right to down
    while(d):
        sc = d.pop()
        seen.add(sc)
        for dx , dy in stepsa:
            nx = sc[0] + dx
            ny = sc[1] + dy
            if 0<= nx < dimx and 0<= ny < dimy and dmap[(nx,ny)] == '#' and (nx,ny) not in seen:
                d.append((nx,ny))
                if nx ==dimx-1:
                    return True
    return False

#we need to find a closed wall either going from left to up, or from right to down, as there is too much space in the middle to go realistically from left to right
def part2():
    #nbyte = 12 #for example
    #dimx, dimy = (7,7)#
    nbyte=1024 
    dimx, dimy = (71,71)
    mp = {(i,j): '.' for i in range(dimx) for j in range(dimy)}
    inpc = list(zip(range(len(inpa)),[(nums(inp)[1] , nums(inp)[0]) for inp in inpa]))
    for i,co in inpc:
        if i < nbyte:
            mp[(co[0],co[1])] = '#'

    for  i, co in inpc[nbyte:]:
        mp[(co[0],co[1])] = '#'
        closed = is_close(mp, dimx, dimy)
        if closed:
            return str(co[1]) + ',' + str(co[0])  #switch back to coordinates used in input (my x is input y, and my y is input x)

def find_steps(mp , dimx, dimy, sc, ec):
    hq = []
    nstep,cost  = 0, dimx + dimy
    heapq.heappush(hq, (cost,nstep , sc))
    seen = set()
    while hq:
        cost, nstep, sc = heapq.heappop(hq)
        nstep +=1
        seen.add(sc)
        for dx , dy in steps:
            nx = sc[0] + dx
            ny = sc[1] + dy
            cost = nstep + (dimx-nx)+(dimy-ny)
            if (nx,ny) == ec:
                print('end reached: ' , cost,nstep, nx,ny)
                break
            if 0<= nx < dimx and 0<= ny < dimy and mp[(nx,ny)] == '.' and (nx,ny) not in seen:
                heapq.heappush(hq, (cost,nstep , (nx,ny)))
        if (nx,ny) == ec:
            break
    return nstep

#after writing the map we notice that there is a lot of space in the middle, but only a few exits of the top left corner and only a few entrances in the bottom right.
#therefore we can divide the problem in an A* from start to exit of bottom left (14,64), + the number of steps to go straightforwardly down to (48,62) = 48-14+64-62 = 36
#plus the n of steps from the end position to the (48,62). (we reverse order as its easier to leave the right corner then to go in it from the correct path.
def part1():
    nbyte=1024 #for part1
    dimx, dimy = (71,71)
    print('dims(x,y):' , dimx ,dimy)
    mp = {(i,j): '.' for i in range(dimx) for j in range(dimy)}
    inpc = list(zip(range(len(inpa)),inpa))
    for i,line in inpc:
        y,x = nums(line)
        if i < nbyte:
            mp[(x,y)] = '#'
    print_map(mp,dimx,dimy)
    sc = (0,0)
    ec = (14,64)
    nstep = find_steps(mp, dimx,dimy, sc,ec)
    sc = (48,62)
    nstep += abs(sc[0] - ec[0]) + abs(sc[1] - ec[1])
    ec = (dimx-1,dimy-1)
    nstep += find_steps(mp, dimx,dimy, ec,sc)
    return nstep

result1 = part1()
result2 = part2()
# Submit
print('Result 1:', result1)
#aoc.submit(1, result1)
print('Result 2:', result2)
#aoc.submit(2, result2)
