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
sys.setrecursionlimit(999999999)
from collections import Counter, defaultdict, deque #defaultdict provides default function when accessing key not present
#For best performancy run this with pypy

with open('input19.txt','r') as aoc:
    text = aoc.read()
inpa , inpb = text.strip().split('\n\n')
stringlist ="""r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
"""
#inpa, inpb = [line for line in stringlist.strip().split('\n\n')]
patl = [p.strip() for p in inpa.split(',')]
print(patl)
e = Counter([len(i) for i in patl])
maxpl = max(e)
print('Max length of a part:' , max(e))

cachel = {}
def test(s):
    #can s be made from the patternlist
    if s in cachel:
        return cachel[s]
    elif len(s) ==0:
        return True
    elif s in patl:
        return True
    else:
        for i in range(1,maxpl+1):
           if s[:i] in patl and test( s[i:] ):
               cachel[s] = True
               return True
    cachel[s] = False
    return False

ncache = {}
def find_cnt(s):
    #find number of ways s can be constructed from valid parts
    if s in ncache:
        return ncache[s]
    vp = 0
    if s in patl:
        vp += 1
    for i in range(1,maxpl+1):
        if s[:i] in patl and test(s[i:]):
            vp += find_cnt(s[i:])
    ncache[s] = vp
    return vp

pcache = {}
def find_parts(s):
    #Returns a list of all possible breakdowns of s in its valid parts. But only works for the example problem :)
    if s in pcache:
        return pcache[s]
    vp = []
    if s in patl:
        vp = [[s]]
    for i in range(1,maxpl+1):
        newl = []
        if s[:i] in patl:
            newl.append(s[:i])
            if test(s[i:]):
                for j in find_parts(s[i:]):
                    if newl + j not in vp:
                        vp.append(newl + j)
            else:
                newl = []
    pcache[s] = vp
    return vp

def parts():
    nval = 0
    nval2 = 0
    des = [b.strip() for b in inpb.split('\n')]
    for i, line in enumerate(des):
        if test(line):
            nval += 1
            #pl = find_parts(line) #returns a list of all possible breakdowns of the line by its valid parts, such that len(pl) == num2, but only works for example problem.
            #print(pl, len(pl))
            num2 = find_cnt(line)
            print(line, num2)
            nval2 += num2
    return nval ,nval2

result1,result2 = parts()
print('Result 1:', result1)
print('Result 2:', result2)
