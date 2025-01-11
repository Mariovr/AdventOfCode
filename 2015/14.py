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
import re
from aoc import AOC

if len(sys.argv) > 1:
    example = open(sys.argv[1]).read().strip()
    inpa = [line.strip() for line in example.strip().split('\n')]
    timelim = 1000 #for example
else:
    aoc = AOC(14 , 2015)
    inpa = aoc.input.strip().split('\n')
    timelim = 2503

nums = lambda s : [int(x) for x in re.findall(r'-?\d+', s)]

res1 = 0
pl = [0] * len(inpa)
for seconds in range(1,timelim+1):
    maxx = 0
    maxi =[]
    for i, line in enumerate(inpa):
        v,t,r = nums(line) #speed, running time , rest time
        x =seconds // (t+r) *t * v + min(seconds % (t+r) , t) * v #distance travelled at seconds
        if x >= maxx:
            if seconds == timelim:
                res1 = x
            if x > maxx:
                maxx= x
                maxi = [i]
            else:
                maxi.append(i)
    for m in maxi: #to account that at some points multiple reindeer can be in the lead.
        pl[m] += 1

print(pl)
print('Result 1:', res1)
print('Result 2:', max(pl))
