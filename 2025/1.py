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
import re
from aoc import AOC

if len(sys.argv) > 1:
    example = open(sys.argv[1]).read().strip()
    inpa = [line.strip() for line in example.strip().split('\n')]
else:
    aoc = AOC(1, 2025)
    inpa = aoc.input.strip().split('\n')

print(inpa)
dist = lambda s : [int(x) for x in re.findall(r'-?\d+', s)][0]

res1, res2 = 0, 0
start, mod = 50, 100

for line in inpa:
    nrot = dist(line)
    if line[0] == 'R':
        start = (start + nrot)
    else:
        start = (start - nrot)

    if  0 >= start or start >= 100: #if we need to apply modulo operator.
        if start >=100 :
            res2 += int(start/100)
        elif start < 0:
            res2 += int(abs(start)/100) +1 #+1 to account when we first pass zero
            if nrot == -1*start : #except if we started from zero then dont need to add 1 when end res is negative.
                res2 -=1
        elif start == 0 :
            res2 += 1

        start = start %100
        if start == 0:
            res1 += 1 #for first exercise just need to count when we end on zero after one modification.

print('Result 1:', res1)
print('Result 2:', res2)
