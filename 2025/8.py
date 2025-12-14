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
from functools import cache, total_ordering, reduce
import re
import heapq as hq #heapify(list) , heappush(heap,item) , heappop(heap, item) returns lowest and removes, merge, nlargest(n, iterable, key=None), nsmallest
from aoc import AOC
from math import sqrt

if len(sys.argv) > 1:
    example = open(sys.argv[1]).read().strip()
    inpa = [line.strip() for line in example.strip().split('\n')]
else:
    aoc = AOC(8 , 2025)
    inpa = aoc.input.strip().split('\n')

nums = lambda s : (int(x) for x in re.findall(r'-?\d+', s))

def dist(cor1, cor2):
    return sqrt(sum([(x1 - x2)**2  for x1 , x2 in zip(cor1, cor2) ]) )

dmap = {}
boxes = []
for i, line in enumerate(inpa):
    ncoor = tuple(nums(line))
    for j, box in enumerate(boxes):
        dindexes = frozenset([i,j])
        dmap[dindexes] = dist(ncoor,  box)
    boxes.append(ncoor)

numconnect = 1000
groups = [[i] for i in range(len(boxes)) ]
for i in range(10000000000000000):
    connect = min(dmap, key= dmap.get)
    indexes = [i for el in connect for i, group in enumerate(groups) if el in group ]
    if indexes[0] != indexes[1]: #only merge groups if elements are not already in the same group 
        if len(groups) == 2:
            res2 = reduce(lambda x, y : x* y , [boxes[el][0]  for el in connect ] )
            break
        groups[indexes[0] ] = groups[indexes[0] ] + groups[indexes[1] ]
        del groups[indexes[1]]
    del dmap[connect]
    if i == numconnect -1:
        res1 = reduce(lambda x, y : x*y ,  hq.nlargest(3,[len(group) for group in groups] ) )

print('Result 1:', res1)
print('Result 2:', res2)
