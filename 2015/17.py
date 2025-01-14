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
sys.setrecursionlimit(99999999)
from collections import defaultdict
from aoc import AOC

if len(sys.argv) > 1:
    example = open(sys.argv[1]).read().strip()
    inpa = [int(line.strip()) for line in example.strip().split('\n')]
    target = 25
else:
    aoc = AOC(17 , 2015)
    inpa = [int(a) for a in aoc.input.strip().split('\n')]
    target = 150

ncon_countways = defaultdict(int)
def find(left, picked, lp):
    if left == 0:
        #print([inpa[i] for i in picked]) #to print out a set of containers that sum up to target
        ncon_countways[len(picked)] += 1
        return 1
    elif left < 0 :
        return 0
    tot = 0
    for i, c in enumerate(inpa):
        if i > lp:
            npick = picked[:] + [i]
            tot += find(left - c, npick, i)
    return tot

res1 = find(target, [],-1)

print('Result 1:', res1)
print('Result 2:',ncon_countways[min(ncon_countways.keys())] )
