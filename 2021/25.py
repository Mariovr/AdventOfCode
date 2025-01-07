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
from aoc import AOC

aoc = AOC(25 , 2021)
inpa = aoc.input.strip().split('\n')
stringlist ="""v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
"""
#inpa = [line.strip() for line in stringlist.strip().split('\n')] #answer is 58
print(inpa)

def move(mp , step , l, dimx , dimy):
    m = []
    for i, c in enumerate(l):
        nx = (c[0] + step[0]) % dimx
        ny = (c[1] + step[1]) % dimy
        if not mp[(nx,ny)]:
            m.append((i, nx,ny,c))

    for i, x, y , c in m:
        l[i] = (x,y)
        mp[(x,y) ] = 1
        mp[c] = 0
    return len(m)

def print_g(mp, dimx , dimy):
    for i in range(dimx):
        s = ''
        for j in range(dimy):
            if mp[(i,j)]:
                s += 'x'
            else:
                s+= '.'

def part1():
    el = []
    sl = []
    print(inpa)
    dimx, dimy = len(inpa), len(inpa[0])
    print('dims(x,y):' , dimx ,dimy)
    mp = defaultdict(lambda: 0)
    for i, line in enumerate(inpa):
        for  j, l in enumerate(list(line)):
            if l != '.':
                mp[(i,j) ] =1
            if l == '>':
                el.append((i,j))
            if l == 'v':
                sl.append((i,j))

    res = 1
    while(True):
        if not (move(mp, (0,1) , el, dimx,dimy) + move(mp, (1,0) , sl,dimx,dimy) ) :
            break
        #print_g(mp, dimx,dimy)
        res += 1
    return res

print('Result 1:', part1())
