# This program is free software. It comes without any warranty, to the extent
# permitted by applicable law. You may use it, redistribute it and/or modify
# it, in whole or in part, provided that you do so at your own risk and do not
# hold the developers or copyright holders liable for any claim, damages, or
# other liabilities arising in connection with the software.
# 
#Developed by Mario Van Raemdonck, 2023;
#
# -*- coding: utf-8 -*-
#! /usr/bin/env python 

import os
import sys
import re
from itertools import combinations
from copy import copy,deepcopy
import random
import networkx as nx  #comment out to use pypy for the karger solution.
sys.setrecursionlimit(10000)

"""
This code contains three solutions to the problem:
1) Using an external package networkx. 
2) A naieve implementation of the Karger algorithm, using the fact that we know the minimal cut is three. (works for both the real and sample problem)
   Ref.: https://web.stanford.edu/class/archive/cs/cs161/cs161.1172/CS161Lecture16.pdf
3) A brute force solution. (works only for the sample problem)
"""
#For solution 1) using networkx.
def min_cut_using_networkx(links):
    G = nx.Graph()
    start = list(deepcopy(links[0]))
    for link in [list(lnk ) for lnk in links]:
        G.add_edge(link[0], link[1], capacity=1.0)
        G.add_edge(link[1], link[0], capacity=1.0)
    cut_value = 100
    while cut_value > 3:
        sam = random.sample(links , 2)
        if list(sam[0])[0] != list(sam[1])[1]:
            cut_value, partition = nx.minimum_cut(G,list(sam[0])[0] , list(sam[1])[1])
    reachable, non_reachable = partition
    print('Cut value is: ' , cut_value)
    #print(reachable)
    #print(non_reachable)
    print('Result with networkx is: ' , len(reachable) *len(non_reachable) )
    cutset = set()
    for u, nbrs in ((n, G[n]) for n in reachable):
        cutset.update((u, v) for v in nbrs if v in non_reachable)
    print('Bounds to cut, to get mincut: ' , sorted(cutset))

#For solution 3) brute force.
def find_all_paths( start, llist, exclude , checked = set()):
    if checked == set(): checked.add(start)
    for nextn in llist[start]:
        if nextn not in checked and set([start,nextn]) not in exclude:
            #print('Node is: ' , nextn)
            checked.add(nextn)
            find_all_paths( nextn,llist, exclude, checked )
    return checked

#For solution 2) Karger algorithm.
def merge(llist, a, b):
    mname = a + b
    aval = llist.pop(a)
    if b in aval:
        aval = [a for a  in aval if a != b]
    bval = llist.pop(b)
    if a in bval:
        bval = [b for b in bval if a != b]

    for key , value in llist.items():
        if a in value and b in value:
            aind =  [i for i in range(len(value)) if value[i] == a]
            for i in aind:
                value[i] =  mname
            bind =  [i for i in range(len(value)) if value[i] == b]
            for i in bind:
                value[i] =  mname
        if a in value:
            aind =  [i for i in range(len(value)) if value[i] == a]
            for i in aind:
                value[i] =  mname
        if b in value:
            bind =  [i for i in range(len(value)) if value[i] == b]
            for i in bind:
                value[i] =  mname

    llist[mname] = aval + bval

def main(args , **kwargs):
    #Load the graph in the internal data structures.
    llist = {}
    for line in args:
        start, end = line.split(':')
        if start in llist.keys():
            llist[start] += end.strip().split(' ')
        else:
            llist[start] =end.strip().split(' ')
        for e in end.strip().split(' '):
            if e in llist.keys():
                llist[e] += [start]
            else:
                llist[e] = [start]

    links = [] #construct list of all pair links.
    for l1 , l2 in llist.items():
        for y in l2:
            d =set([l1,y])
            if d not in links:
                links.append(d) # link has no order.

    #1) Solution using networkx.
    min_cut_using_networkx(links)

    #2) Solution using the Karger algorithm (works for both the sample and real problem).
    cutsize = 100
    while( cutsize != 3.):
        nllist = deepcopy(llist)
        while(len(nllist) > 2):
            a = random.sample(list(nllist.keys()) , 1)[0]
            b =max(nllist[a],key=nllist[a].count)
            merge(nllist, a,b)

        cutsize = len(list(nllist.values())[0])
        print('Cutsize: ' , cutsize)
    res = 1
    for i in nllist.keys():
        res *= len(i)/3.
    print('Result with Karger is: ' , res)

    #3) Brute force solution (works only for sample problem)
    for x,y,z in combinations(links , 3):
        exclude = [x,y,z]
        #If the excluded edges lead to disjoint sets, each part of the edge will be in one of the disjoint set.
        test= list(x)
        result = find_all_paths(test[0],llist , exclude  , set())  
        result2 = find_all_paths(test[1],llist , exclude, set() ) 
        if set(result).isdisjoint(set(result2)):
            print('Found two disjoint sets: ' , result , result2)
            break

    print('Disjoint set1: ' , result)
    print('Disjoint set2: ' , result2)
    result =len(result)*len(result2)
    print('Result with brute force solution is: ' ,result)

    return result

if __name__ == "__main__":
    stringlist ="""jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
"""

    print('Start to solve sample problem: ')
    lines = [line.strip() for line in stringlist.strip().split('\n')]
    print(lines)
    assert main(lines) == 54

    print('Start to solve real problem: ')
    file = "inputday25.txt"
    with open(file,'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    result = main(lines)
    print('Result is: ', result)
