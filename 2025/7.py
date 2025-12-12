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
import heapq as hq #heapify(list) , heappush(heap,item) , heappop(heap, item) returns lowest and removes, merge, nlargest(n, iterable, key=None), nsmallest
from collections import Counter, defaultdict, deque #defaultdict provides default function when accessing key not present
from aoc import AOC

if len(sys.argv) > 1:
    example = open(sys.argv[1]).read().strip()
    inpa = [line.strip() for line in example.strip().split('\n')]
else:
    aoc = AOC(7 , 2025)
    inpa = aoc.input.strip().split('\n')

X, Y = len(inpa), len(inpa[0])
print('dims(x,y):' , X ,Y)

mp = {}
for i, line in enumerate(inpa):
    for  j, char in enumerate(list(line)):
        mp[(i,j)] = char
        if char == 'S':
            scoord = (i,j)

h = deque([(0,scoord,1)])
seen_sp = set()
seen_loc = {}
lev = 0
totcnt = 0
while (True):
    if h:
        xdim , sc, cnt = h.popleft()
        nsc = (sc[0] + 1 , sc[1] )
        if nsc[0] == X:
            h.append((xdim , sc , cnt) )
            break

        if nsc in seen_loc.keys():
            seen_loc[nsc] += cnt
        elif not (0<= nsc[0] < X) or not (0<= nsc[1] < Y):
            totcnt += cnt
            pass
        elif mp[nsc] == '^': 
            if (nsc[0] , nsc[1] - 1) not in seen_loc:
                seen_loc[(nsc[0] , nsc[1] - 1) ]  = cnt
            else:
                seen_loc[(nsc[0] , nsc[1] - 1) ]  += cnt
            if (nsc[0] , nsc[1] + 1) not in seen_loc:
                seen_loc[(nsc[0] , nsc[1] + 1) ] = cnt
            else:
                seen_loc[(nsc[0] , nsc[1] + 1) ] += cnt
            seen_sp.add(nsc)
        else:
            seen_loc[(nsc[0] , nsc[1])]  = cnt
    else:
        lev +=1
        h = deque([])
        for k , v in seen_loc.items():
            h.append((lev , k , v) )
        seen_loc = {}

print('Result 1:', len(seen_sp))
print('Result 2:', sum([x[2] for x in h if x[0] == X-1]) + totcnt)
