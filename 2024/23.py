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
from itertools import combinations
from aoc import AOC
aoc = AOC(23 , 2024)
inpa = aoc.input.strip().split('\n')

def parts():
    #Load the graph into the internal data structure.
    llist = {}
    for line in inpa:
        start, end = line.split('-')
        if start in llist.keys():
            llist[start] += [end.strip()]
        else:
            llist[start] = [end.strip()]
        if end in llist.keys():
            llist[end] += [start]
        else:
            llist[end] = [start]

    res1, res2 = 0, ''
    seen = set()
    for i, coni in llist.items():
        if i.startswith('t'):
            for j, node1 in enumerate(coni):
                for node2 in coni[j+1:]:
                    if node2 in llist[node1]:
                        d = [i,node1,node2]
                        d.sort()
                        if tuple(d) not in seen:
                            seen.add(tuple(d))
                            res1 += 1

    maxn = max([len(coni) for i, coni in llist.items() ] ) #maxnumber of nodes linked to a particular node.
    print('max number of nodes linked to a part node: ' , maxn)
    for n in range(maxn, -1 , -1 ): #search for largest set of strongly connected nodes, if we cant find n strongly connected nodes, reduce n by one and try again, first set encountered will be the max set. 
        for i, coni in llist.items():
            setl = []
            setl.append(set([i] + coni) )
            for node1 in coni:
                setl.append(set(llist[node1] + [node1]) )
            for comb in combinations(range(len(setl)), n ) :
                intersection_set = set.intersection(*[s for i, s in enumerate(setl) if i in comb])
                if len(intersection_set) == n:
                    print('Max number of strongly connected nodes: ', len(intersection_set)) 
                    lanpcomps = list(intersection_set)
                    res2 = ','.join(sorted(lanpcomps))
                    return res1, res2

result1,result2 = parts()
print('Result 1:', result1)
print('Result 2:', result2)
