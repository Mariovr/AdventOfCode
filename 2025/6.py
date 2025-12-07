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
    example = open(sys.argv[1]).read()[:-1]
    inpa = [line for line in example.split('\n')]
else:
    aoc = AOC(6 , 2025)
    inpa = aoc.input.split('\n')[:-1]

X = len(inpa)
nums = lambda s : [int(x) for x in re.findall(r'-?\d+', s)]

probs = []
ops = []
cnum = []
for i, line in enumerate(inpa):
    if i < X - 1:
        probs.append( line)
    else:
        ops = line.split()
        for  s , e in zip([m.start() for m in list(re.finditer(r'[*+]', line))] , [m.start()+1 for m in list(re.finditer(r'[*+]', line[1:]))] + [len(line)+1]): #+1 to account for index of line vs line[1:]
            cnum.append((s,e-2, e-2-s+1)) #probstart, probend , size

res1, res2 = 0,0
for i, op in enumerate(ops):
    if op == '*':
        res = 1
        for prob in probs:
            res *= nums(prob)[i]
        res1 += res
        res = 1
    else:
        res = 0
        for prob in probs:
            res += nums(prob)[i]
        res1 += res
        res = 0

    s, e, sz = cnum[i] #start to solve 2nd problem
    for j in range(sz):
        num = ''
        for k  in range(X-1):
            num += probs[k][s+j]
        if op == '*':
            res *= int(num)
        else:
            res += int(num)
    res2 += res

print('Result 1:', res1)
print('Result 2:', res2)
