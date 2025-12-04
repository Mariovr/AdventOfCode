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
    aoc = AOC(4 , 2025)
    inpa = aoc.input.strip().split('\n')

X, Y = len(inpa), len(inpa[0])
print('dims(x,y):' , X ,Y)

steps = [[0, 1], [1, 0], [0, -1], [-1, 0]]
stepsa = [[1, 1], [-1, -1], [1, -1], [-1, 1]] + steps

mp =  {}
for i, line in enumerate(inpa):
    for  j, char in enumerate(list(line)):
        if char == '@':
            mp[(i,j)] = char
print(mp)

res1,res2,remove = 0,0, True
while(remove):
    remlist = []
    for i , j in  mp.keys():
        numocc = 0
        for step in stepsa:
            if (i + step[0] , j + step[1] ) in mp.keys() and mp[(i + step[0] , j + step[1] )] == '@':
                numocc +=1
        if numocc < 4:
            res2 += 1
            remlist.append((i,j))
    if res1 == 0:
        res1 = res2
    if len(remlist) > 0:
        for i,j in remlist:
            del mp[(i,j)]
    else:
        remove = False

print('Result 1:', res1)
print('Result 2:', res2)
