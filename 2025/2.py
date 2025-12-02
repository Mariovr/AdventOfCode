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
    inpa = [line.strip() for line in example.strip().split(',')]
else:
    aoc = AOC(2 , 2025)
    inpa = aoc.input.strip().split(',')
print(inpa)
nums = lambda s : (int(x) for x in re.findall(r'\d+', s))

res1,res2 = 0,0
inval = set()
for i, line in enumerate(inpa):
    s,e = nums(line)
    for i in range(s,e+1):
        ndig = len(str(i))
        for j in range(2,ndig+1):
            invalid = True
            if ndig %j == 0:
                test = str(i)[:ndig//j]
                for k in range(j-1):
                    if test != str(i)[ndig//j*(k+1):ndig//j*(k+2)] :
                        invalid = False
                if invalid:
                    inval.add(i)
                    if j == 2:
                        res1 += i

#print(inval)
res2 = sum(inval)

print('Result 1:', res1)
print('Result 2:', res2)
