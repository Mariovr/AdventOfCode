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

def test_c(newc, gmap,e):
    try:
        it = gmap[newc] 
    except KeyError:
        it = '#'
    if  it == '.' :
        e.add(newc)

def main(args , **kwargs):
    gmap = {}
    result = 0
    numstep = 64 #numstep = 6 for sample problem.
    numstep = 10000
    startc = (0,0)

    for ind , line in enumerate(args):
        sp = re.search(r'S' , line)
        if sp:
            startc = (ind , sp.start() )
        gmap.update( {(ind,i):ch for i,ch in enumerate(line)} )

    #print(gmap)
    
    gmap[startc] = '.'
    d = set([startc])
    #print(d)
    for i in range(numstep):
        e = set()
        for coord in d:
            for newc in [(coord[0] + 1, coord[1]),(coord[0] -1, coord[1]),(coord[0] , coord[1]+1),(coord[0], coord[1]-1)]:
                test_c(newc,gmap,e)
            #print(e)
        d = e
        print('At step: ' , i+1 , 'we have pos occupied: ' , len(d))

    result = len(d)
    return result

if __name__ == "__main__":
    stringlist ="""...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
"""
#    lines = [line.strip() for line in stringlist.strip().split('\n')]
#    print(lines)
#    assert main(lines) == 16
#
    file = "inputday21.txt"
    with open(file,'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    result = main(lines)
    print('Result is: ', result)



