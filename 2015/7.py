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
    aoc = AOC(7 , 2015)
    inpa = aoc.input.strip().split('\n')
print(inpa)

C= {}
def find(output , mp):
    res = 0
    if output in C:
        return C[output]
    elif isinstance(mp[output],int):
        res =  mp[output]
    else:
        evals = mp[output]
        if len(evals) == 1:
            res =  find(evals[0],mp)
        elif len(evals) == 2:
            if evals[1].isnumeric():
                res =  ~int(evals[1])
            else:
                res =  ~find(evals[1],mp)
        elif len(evals) ==3:
            if  evals[1].isnumeric():
                anum = int(evals[1])
            else:
                anum = find(evals[1],mp)
            if evals[2].isnumeric():
                bnum = int(evals[2])
            else:
                bnum = find(evals[2],mp)
            res = evals[0](anum , bnum)
    C[output] = res
    return res

def parts():
    ops = {'NOT' : lambda x : ~x , 'OR': lambda x,y : x | y , 'AND' : lambda x,y : x & y , 'LSHIFT' : lambda x , y: x << y, 'RSHIFT' : lambda x,y : x>> y }
    mp = {}
    for line in inpa:
        words = line.split(' ')
        if len(words) == 3:
            try:
                inw = int(words[0])
                mp[words[2]] = inw
            except ValueError:
                mp[words[2]] = [words[0] ]
        elif len(words) == 4:
            mp[words[3] ] = [ops[words[0]] , words[1] ]
        else:
            mp[words[4] ] = [ops[words[1]] , words[0], words[2 ] ]

    res1 = find('a', mp)
    C.clear()
    C['b'] = res1
    res2 = find('a', mp)
    return res1, res2

result1,result2 = parts()
print('Result 1:', result1)
print('Result 2:', result2)
