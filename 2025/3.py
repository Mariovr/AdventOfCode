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
    aoc = AOC(3 , 2025)
    inpa = aoc.input.strip().split('\n')

print(inpa)

res1,res2 = 0,0
for i, line in enumerate(inpa):
    res1 += int(max(line[:-1]) + max(line[line.index(max(line[:-1]))+1:] ))
    joltage = ''
    for j in range(11,0  , -1):
        fel_idx = line.index(max(line[:(-j)]))
        joltage = joltage + line[fel_idx]
        line = line[fel_idx +1 : ]
    joltage = joltage + max(line)
    res2 += int(joltage)

print('Result 1:', res1)
print('Result 2:', res2)
