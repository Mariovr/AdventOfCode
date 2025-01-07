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
import hashlib

if len(sys.argv) > 1:
    example = open(sys.argv[1]).read().strip()
    inpa = [line.strip() for line in example.strip().split('\n')]
else:
    aoc = AOC(4 , 2015)
    inpa = aoc.input.strip().split('\n')
print(inpa)

def parts():
    res1, res2 = 0,0
    for i in range(0, 500000000):
        s = inpa[0] + str(i)
        hashinput = s.encode()
        d = hashlib.md5(hashinput)
        #print(d.hexdigest())
        if d.hexdigest().startswith('0'*5) and res1 == 0:
            res1 = i
        if d.hexdigest().startswith('0'*6):
            res2 = i
            break

    return res1, res2

result1, result2 = parts()
print('Result 1:', result1)
print('Result 2:', result2)
