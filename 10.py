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

def move(pos , dmap, xdim , ydim, startc, endset):
    stepl = [(-1,0), (0,1),(1,0),(0,-1) ]
    npos = (0,0)
    oldval = dmap[pos[0] ] [pos[1] ]
    for step in stepl:
        npos = (pos[0] + step[0],pos[1] + step[1])
        if 0 <= npos[0] < xdim and 0 <= npos[1] < ydim:
            nval =dmap[npos[0] ] [npos[1]] 
            if  nval == (oldval +1):
                if nval != 9:
                    startc = move(npos , dmap, xdim,ydim, startc, endset)
                else:
                    startc += 1
                    endset.add(npos)
    return startc

def main(args , **kwargs):
    dmap = []
    xdim = len(args)
    ydim = len(args[0])

    startp = []
    for i, line in enumerate(args):
        row = []
        for j, pos in enumerate(line):
            if pos == '0' :
                startp.append((i,j))
            row.append(int(pos))
        dmap.append(row)

    result1 = 0
    result2 = 0
    for spos in startp:
        endset = set()
        result2 += move(spos, dmap , xdim ,ydim ,0, endset)
        result1 += len(endset)
    print('Result 1:' , result1)
    print('Result 2:' , result2)
    return result2

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
    assert main(lines) == 81

    file = "input10.txt"
    with open(file,'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    result = main(lines)
    print('Result is: ', result)
