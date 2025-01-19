# This program is free software. It comes without any warranty, to the extent
# permitted by applicable law. You may use it, redistribute it and/or modify
# it, in whole or in part, provided that you do so at your own risk and do not
# hold the developers or copyright holders liable for any claim, damages, or
# other liabilities arising in connection with the software.
# 
#Developed by Mario Van Raemdonck, 2025;
#
# -*- coding: utf-8 -*-
#! /usr/bin/env python 
import sys
from aoc import AOC

if len(sys.argv) > 1:
    example = open(sys.argv[1]).read().strip()
    inpa = [line.strip() for line in example.strip().split('\n')]
else:
    aoc = AOC(18 , 2015)
    inpa = aoc.input.strip().split('\n')

X, Y = len(inpa), len(inpa[0])
print('dims(x,y):' , X ,Y)
stepsa = [[1, 1], [-1, -1], [1, -1], [-1, 1],[0, 1], [1, 0], [0, -1], [-1, 0]]

mp = {}
for i, line in enumerate(inpa):
    for  j, char in enumerate(list(line)):
        mp[(i,j)] = char
mp2 = mp

def step_lmap(mp):
    nmp = {}
    for i in range(X):
        for j in range(Y):
            cnton = 0
            for step in stepsa:
                nx = i + step[0]
                ny = j + step[1]
                if 0<= nx < X and 0<= ny < Y and mp[(nx,ny)] == '#':
                    cnton +=1
            if mp[(i,j)] == '#' and cnton not in [2,3]:
                nmp[(i,j)] = '.'
            elif mp[(i,j)] == '.' and cnton in [3]:
                nmp[(i,j)] = '#'
            else:
                nmp[(i,j)] =mp[(i,j)]
    return nmp

nstep = 100
for n in range(nstep):
    mp = step_lmap(mp)
    for pos in [(0,0), (0,Y-1) , (X-1,0) , (X-1,Y-1)]: #For part 2 the lights in the corners are always on.
        mp2[(pos[0],pos[1])] = '#'
    mp2 = step_lmap(mp2)

res1,res2 = 0,0
for i in range(X):
    for j in range(Y):
        if mp[(i,j)] == '#':
            res1 += 1
        if mp2[(i,j)] == '#' or (i,j) in [(0,0), (0,Y-1) , (X-1,0) , (X-1,Y-1)]:
            res2 += 1

print('Result 1:', res1)
print('Result 2:', res2)
