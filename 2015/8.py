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
    inpa = [line.strip() for line in example.split('\n')]
else:
    aoc = AOC(8,2015)
    inpa = aoc.input.strip().split('\n')
print(inpa)

def part1():
    tres = 0
    for line in inpa:
        mline = re.sub(r'\\\\' , 'Z' , line)
        mline = re.sub(r'\\"(?!$)' , 'Y',mline) #nice example of a negative lookbehind
        mline = re.sub(r'\\x[A-Fa-f\d]{2}' , 'X', mline)
        mline = mline.replace('"' , '')
        tres += len(line) - len(mline)
    return tres

def part2():
    tres = 0
    for line in inpa:
        mline = re.sub(r'\\' , r'\\\\', line)
        mline = re.sub(r'"' , r'\\"',mline)
        mline = '"' + mline + '"' 
        tres += len(mline) - len(line)
    return tres

result1 = part1()
result2 = part2()
print('Result 1:', result1)
print('Result 2:', result2)
