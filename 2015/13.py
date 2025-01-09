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
from collections import deque
from aoc import AOC

if len(sys.argv) > 1:
    example = open(sys.argv[1]).read().strip()
    inpa = [line.strip() for line in example.strip().split('\n')]
else:
    aoc = AOC(13 , 2015)
    inpa = aoc.input.strip().split('\n')

#to search for the maximum happiness
def bfs(people, hapcost):
    hapmax = 0
    startp = people[0]
    Q = deque([ (0, startp, list() )]) #tot dist, current city, cities visited (starting from random start city)
    while len(Q) > 0:
        chap , cur, pvis = Q.pop()
        pvis.append(cur)
        if  len(pvis) == len(people):
            nhap = chap + hapcost[(startp, cur)] + hapcost[(cur,startp)]
            if  nhap > hapmax:
                hapmax = nhap
                optseats = pvis
        for ahap, adj in [(hapcost[(cur,nper)]+ hapcost[(nper,cur)], nper) for nper in people if nper not in pvis]:
            Q.append((chap + ahap, adj, pvis[:]))
    print(optseats)
    return hapmax

hapcost = {}
people = []
for line in inpa:
    p1, action, val1, p2 = re.search(r'^(\w+)\swould\s(\w+)\s(\d+).*?(\w+).$', line).groups()
    if p1 not in people:
        people.append(p1)
    if action == 'gain':
        hapcost[(p1,p2)] = int(val1)
    else:
        hapcost[(p1,p2) ] = -1*int(val1)

res1 = bfs(people,hapcost)

for person in people:
    hapcost[(person,'Me')] = 0
    hapcost[('Me', person)] = 0
people.append('Me')

res2 = bfs(people,hapcost)

print('Result 1:', res1)
print('Result 2:', res2)
