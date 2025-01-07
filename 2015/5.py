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

if len(sys.argv) > 1:
    example = open(sys.argv[1]).read().strip()
    inpa = [line.strip() for line in example.strip().split('\n')]
else:
    aoc = AOC(5 , 2015)
    inpa = aoc.input.strip().split('\n')
print(inpa)

def is_nice(s):
    bad = ['ab','cd','pq','xy']
    vowel = list('aeiou')
    for b in bad:
        if b in s:
            return False
    cnt = 0
    for v in vowel:
        cnt += s.count(v)
    if cnt < 3:
        return False
    for i in range(len(s) -1):
        if s[i] == s[i+1]:
            return True
    return False

def is_nice2(s):
    rep , pair = False, False
    for i in range(0,len(s) -2):
        f = s[i:i+2]
        if f in s[i+2:]:
            pair = True
        if s[i] == s[i+2]:
            rep = True
    if rep and pair:
        return True
    else:
        return False

def parts():
    res1,res2 = 0,0
    for line in inpa:
        if is_nice(line):
            res1 += 1
        if is_nice2(line):
            res2 += 1
    return res1 , res2

result1,result2 = parts()
print('Result 1:', result1)
print('Result 2:', result2)
