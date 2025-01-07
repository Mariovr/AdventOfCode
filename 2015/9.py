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
from collections import Counter, defaultdict, deque #defaultdict provides default function when accessing key not present
from aoc import AOC

if len(sys.argv) > 1:
    example = open(sys.argv[1]).read().strip()
    inpa = [line.strip() for line in example.strip().split('\n')]
else:
    aoc = AOC(9 , 2015)
    inpa = aoc.input.strip().split('\n')
print(inpa)

def parts():
    mp = defaultdict(list)
    for i, line in enumerate(inpa):
        c1, d, c2, e, r = line.split(' ')
        mp[c1].append((int(r), c2))
        mp[c2].append((int(r), c1))

    res1, res2 = 1e6, 0
    for i in range(len(mp.keys())):
        d = deque([ (0, list(mp.keys())[i], set() )]) #tot dist, current city, cities visited (starting from random start city)
        while len(d) > 0:
            dist , cur, cvis = d.pop()
            cvis.add(cur)
            if  len(cvis) == len(mp.keys()):
                if dist < res1:
                    res1 = dist
                elif dist > res2:
                    res2 = dist
            for nd , adj in mp[cur]:
                if adj not in cvis:
                    d.append((dist+nd , adj, cvis.copy()))
    return res1,res2

res1, res2 = parts()
print('Result 1:', res1)
print('Result 2:', res2)
