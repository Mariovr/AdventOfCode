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
from aoc import AOC

if len(sys.argv) > 1:
    example = open(sys.argv[1]).read().strip()
    inpa = [line.strip() for line in example.strip().split('\n')]
else:
    aoc = AOC(10 , 2015)
    inpa = aoc.input.strip().split('\n')
print(inpa)

def parts():
    res1 = 0
    newl = [int(a) for  a in list(inpa[0])]
    for j in range(50):
        line = newl
        newl = []
        i = 0
        while(i < len(line)):
            c = line[i]
            cnt = 0
            while(i< len(line) and line[i] == c):
                cnt += 1
                i+= 1
            newl += [cnt,c]
        if j == 39:
            res1 = len(newl)
    return res1, len(newl)

result1, result2 = parts()
print('Result 1:', result1)
print('Result 2:', result2)
