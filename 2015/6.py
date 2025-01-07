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
import re
from aoc import AOC

aoc = AOC(6 , 2015)
inpa = aoc.input.strip().split('\n')
print(inpa)

nums = lambda s : [int(x) for x in re.findall(r'-?\d+', s)]

def parts(p2 = False):
    mp = [[0 for i in range(1000) ] for j in range(1000) ]
    for i, line in enumerate(inpa):
        x1,y1, x3, y3 = nums(line)
        d = re.search(r'^([a-zA-Z\s]*)', line)
        if d[0].strip() == 'turn on':
            for d in range(x1, x3+1):
                for e in range(y1, y3+1):
                    if p2:
                        mp[d][e] += 1
                    else:
                        mp[d][e] = 1
        elif d[0].strip() == 'turn off':
            for d in range(x1, x3+1):
                for e in range(y1, y3+1):
                    if p2:
                        mp[d][e] = max(0, mp[d][e]-1 )
                    else:
                        mp[d][e] = 0
        elif d[0].strip() == 'toggle':
            for d in range(x1, x3+1):
                for e in range(y1, y3+1):
                    if p2:
                        mp[d][e] += 2
                    else:
                        mp[d][e] = (mp[d][e] + 1) % 2
    res = 0
    for i in range(1000):
        for j in range(1000):
            res += mp[i][j]
    return res

result1 = parts()
result2 = parts(p2=True)
print('Result 1:', result1)
print('Result 2:', result2)
