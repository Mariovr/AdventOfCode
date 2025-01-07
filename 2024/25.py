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
    inpa = [line for line in example.strip().split('\n\n')]
else:
    aoc = AOC(25 , 2024)
    inpa  = aoc.input.strip().split('\n\n')

def part():
    res, collim = 0,0
    keyl,lockl = [], []
    for item in inpa:
        it = item.split('\n')
        counts = []
        for i in range(len(it[0])):
            col  = [ it[j][i] for j in range(len(it))]
            collim = len(col)
            counts.append(col.count('#'))
        if it[0][0] == '#':
            lockl.append(counts)
        else:
            keyl.append(counts)

    for key in keyl:
        for lock in lockl:
            fit = True
            for i in range(len(key)):
                if key[i] + lock[i] > collim:
                    fit = False
            if fit:
                res += 1
    return res

result1 = part()
print('Result 1:', result1)
