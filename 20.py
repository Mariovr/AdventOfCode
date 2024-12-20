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
from collections import Counter, defaultdict, deque #defaultdict provides default function when accessing key not present
from copy import deepcopy
import re
import heapq #heapify(list) , heappush(heap,item) , heappop(heap, item) returns lowest and removes, merge, nlargest(n, iterable, key=None), nsmallest

with open('input20.txt','r') as aoc:
    text = aoc.read()
inpa = text.strip().split('\n')
#inpa , inpb = aoc.input.strip().split('\n\n')
stringlist ="""###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""
#inpa = [line for line in stringlist.strip().split('\n')]
#inpa, inpb = [line for line in stringlist.strip().split('\n\n')]
print(inpa)

steps = [[0, 1], [1, 0], [0, -1], [-1, 0]]
stepsa = [[1, 1], [-1, -1], [1, -1], [-1, 1]] + steps
steps3d = [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]
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

class Pos(object):
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return (self.value) == (other.value)

    def __lt__(self, other):
        return (self.value) < (other.value)

    def __str__(self):
        outputstr = 'Value: ' + str(self.value) + '\n'
        return outputstr

def f_pathl(mp,sc,ec, dimx , dimy):
    d = deque([])
    nstep =0
    d.append((nstep,sc,(0,0))) #start c , pos, cheat
    seen = set(sc)
    while(d):
        ostep , sc, ch = d.popleft()
        for i, step in enumerate(steps):
            npos = (sc[0] + step[0],sc[1] + step[1])
            if 0 <= npos[0] < dimx and 0 <= npos[1] < dimy and mp[(npos[0],npos[1])] == '.': 
                nstep = ostep + 1
                if npos not in seen:
                    d.append((nstep,npos , ch))
                    seen.add(npos)
                if npos  == ec:
                    sc = npos
                    break
        if sc == ec:
            break
    return nstep

def f_path(mp,sc,ec, dimx , dimy):
    d = deque([])
    nstep =0
    d.append((nstep,sc,(0,0))) #start c ,pos, cheat
    path = {}
    path[sc] = 0
    seen = set()
    seen.add(sc)
    while(d):
        ostep , sc, ch = d.popleft()
        for i, step in enumerate(steps):
            npos = (sc[0] + step[0],sc[1] + step[1])
            if 0 <= npos[0] < dimx and 0 <= npos[1] < dimy and mp[(npos[0],npos[1])] == '.': 
                nstep = ostep + 1
                if npos not in seen:
                    d.append((nstep, npos, ch))
                    seen.add(npos)
                    path[npos] = nstep
                if npos  == ec:
                    sc = npos
                    break
        if sc == ec:
            break
    return path, nstep

def part1():
    res = 0
    dimx, dimy = len(inpa), len(inpa[0])
    print('dims(x,y):' , dimx ,dimy)
    mp = {}
    sc, ec =(0,0) , (0,0)
    wl = []
    pl = []
    for i, line in enumerate(inpa):
        for  j, l in enumerate(list(line)):
            mp[(i,j)] = l
            if l == 'S':
                sc = (i,j)
                mp[(i,j)] = '.'
            if l =='E':
                ec = (i,j)
                mp[(i,j)] = '.'
            if 0 < i < dimx -1 and 0 < j < dimy -1 and l == '#':
                wl.append((i,j))
            if 0 < i < dimx -1 and 0 < j < dimy -1 and l in ('.' , 'E', 'S'):
                pl.append((i,j))
    print('s' , sc)
    print('e' , ec)
    print('numwalls:' , len(wl))
    print('numpoints:' , len(pl))
    chl = defaultdict(set) #contains all cheats, together with steps they save.
    opath , spl= f_path(mp,sc,ec,dimx,dimy)
    print(opath)
    cl = 20
    print('start path length: ' ,spl)
    for i, (w1,w2) in enumerate([p for p in opath.keys()]):
        chs = opath[w1,w2]
        d = deque([(0,w1,w2)]) #chstep , px , py
        seen = set()
        while(d):
            stepsc , x,y = d.popleft()
            for ns, (dx,dy) in enumerate(steps):
                npx = x + dx
                npy = y + dy
                nsc = stepsc + 1
                if 0 <= npx < dimx  and 0 <= npy < dimy and (npx,npy) not in seen:
                    seen.add((npx,npy))
                    if nsc < cl:
                        d.append((nsc,npx,npy))
                    if (npx,npy) in pl:
                        nstep = opath[ (npx,npy)]
                        if (spl - nstep) + chs + nsc < spl:  #cheat saved steps
                            chl[nstep - nsc - chs].add((w1,w2, npx,npy))
                            if nstep-nsc-chs >= 100:
                                res +=1
        print('it:' , i , 'res: ' , res)
    for k , v in chl.items():
        print('dif: ' , k , 'num cheats: ' , len(v))
    return res

result1 = part1()
#result2 = part2()
# Submit
print('Result 1:', result1)
#aoc.submit(1, result1)
#print('Result 2:', result2)
#aoc.submit(2, result2)

