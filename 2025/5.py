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
    inpa, inpb = [line for line in example.strip().split('\n\n')]
else:
    aoc = AOC(5 , 2025)
    inpa , inpb = aoc.input.strip().split('\n\n')

inpa = [a.strip() for a in inpa.split('\n')]
inpb = [b.strip() for b in inpb.split('\n')]

nums = lambda s : [int(x) for x in re.findall(r'\d+', s)]

rangel = []
for line in inpa:
    ran = nums(line)
    for start, end  in rangel:
        if ran[1] < start or ran[0] > end:
            continue
        elif ran[1] >= start and ran[1] <= end and ran[0] < start:
            ran[1] = start -1
        elif ran[0] >= start and ran[0] <= end:
            if ran[1] <= end:
                ran[0] = -1
                break
            else:
                ran[0] = end +1
        else: #ran[0] < start and ran[1] > end -> leads to two new intervals
            rangel.append([ran[0], start-1] )
            ran[0] = end +1
    if ran[0] != -1:
        rangel.append(ran)

res1 = 0
for line in inpb:
    nid = nums(line)[0]
    for ran in rangel:
        if nid <= ran[1] and nid >= ran[0]:
            res1 += 1
            break

res2 = 0
for s, e in rangel:
    res2  += e-s+1

print('Result 1:', res1)
print('Result 2:', res2)
