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

import os
import sys
sys.setrecursionlimit(999999999)
from copy import deepcopy
import re

class Game(object):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        outputstr = 'Value: ' + str(self.value) + '\n'
        return outputstr

def move(pos , dmap, xdim , ydim, nset):
    stepl = [(-1,0), (0,1),(1,0),(0,-1) ]
    npos = (0,0)
    oldval = dmap[pos[0] ] [pos[1] ]
    for step in stepl:
        npos = (pos[0] + step[0],pos[1] + step[1])
        if 0 <= npos[0] < xdim and 0 <= npos[1] < ydim:
            nval =dmap[npos[0] ] [npos[1]] 
            if  nval == (oldval +1):
                if nval != 9:
                    nset.update( move(npos , dmap, xdim,ydim,nset))
                else:
                    print('9 found')
                    nset.add(npos) 
    return nset

def main(args , **kwargs):
    result = 0

    dmap = []
    xdim = len(args)
    ydim = len(args[0])
    stepl = [(-1,0), (0,1),(1,0),(0,-1) ]

    startp = []
    for i, line in enumerate(args):
        row = []
        for j, pos in enumerate(line):
            if pos == '0' :
                startp.append((i,j))
            row.append(int(pos))
        dmap.append(row)

    for spos in startp:
        print('startp: ' ,spos)
        result += len(move(spos, dmap , xdim ,ydim ,set()))
        print('result: ' , result)

    return result

if __name__ == "__main__":
    stringlist ="""89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""

    lines = [line.strip() for line in stringlist.strip().split('\n')]
    print(lines)
    assert main(lines) == 36

    file = "input10.txt"
    with open(file,'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    result = main(lines)
    print('Result is: ', result)
