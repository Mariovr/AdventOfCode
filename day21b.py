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

def test_c(newc, gmap,e, fy, fx):
    it = gmap[newc] 
    if  it == '.' :
        add = (newc,fy,fx)
        e.add(add)

#If all pos in a square are reached once it will fluctuate between the odd (reachable) and even (reachable), num of positions in that square (using sol a: 7748 (even) and 7757 (odd).
#start position is in the exact middle coordinates: (65,65) and dimensions of square are (131,131). There are straight paths from start to next squares in all 4 directions (and also diagonally).
#So surface to consider will be a square of 26501365 size in all directions. It will contain many full squares, 4 tips, and then interchanging small and big parts of a square.
#After 65 steps we reach the next squares in square space. After 65 + 131 = 196 again the next squares with new max/min in square coordinate space, and so on...
#Luckely the input makes it easy for us so we dont need to calculate the special cases on the boundaries (using differences).
#26501365 = 65 + 131 * 202300. 

#(y,x, field vert,field hor)
def main(args , **kwargs):
    gmap = {}
    result = 0
    numstep = 26501365 #numstep = 6 for sample problem.
    numstep = 5000 #numstep = 6 for sample problem.
    startc = (0,0, 0 , 0)

    vdim = len(args)
    hdim = len(args[0])
    ndots = 0
    for ind , line in enumerate(args):
        sp = re.search(r'S' , line)
        ndots += line.count('.')
        if sp:
            startc = ((ind , sp.start()) , 0 , 0)
            #startc = (ind , sp.start() )
        gmap.update( {(ind,i):ch for i,ch in enumerate(line)} )

    
    ndots += 1 #to account start dot
    print('Numdots: ' , ndots)
    gmap[startc[0]] = '.'
    d = set([startc])
    print(d)
    savesol = 0
    for i in range(numstep):
        e = set()
        for coord , fy , fx in d:
            for newc in [( (coord[0] + 1) , coord[1]),((coord[0] -1) , coord[1]),(coord[0] , (coord[1]+1)  ),(coord[0], (coord[1]-1)  )]:
                if newc[0] == vdim:
                    test_c((newc[0] % vdim , newc[1]),gmap,e, fy+1,fx)
                elif newc[0] == -1:
                    test_c((newc[0] % vdim , newc[1]),gmap,e, fy-1,fx)
                elif newc[1] == hdim:
                    test_c((newc[0]  , newc[1] %hdim),gmap,e, fy,fx+1)
                elif newc[1] == -1:
                    test_c((newc[0] , newc[1]%hdim),gmap,e, fy,fx-1)
                else:
                    test_c((newc[0] , newc[1]),gmap,e, fy,fx)

            #print(e)
        d = e
        #if (i+1) %2==1 and (((i +1) - 65) % 131) ==0: #only interested in odd square surfaces and at the points where we start a new square (new max fy or fy).
        print('At step: ' , i , 'we have pos occupied: ' , len(d))
        print('dif' , len(d) - savesol)
        print('At step: ' , i , 'we have max fy: ' , max(d, key = lambda x : x[1]))
        print('At step: ' , i , 'we have max fx: ' , max(d, key = lambda x : x[2]))
        print('At step: ' , i , 'we have min fy: ' , min(d, key = lambda x : x[1]))
        print('At step: ' , i , 'we have min fx: ' , min(d, key = lambda x : x[2]))
        savesol = len(d)

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
#    assert main(lines) == 16733044
#
    file = "inputday21.txt"
    with open(file,'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    result = main(lines)
    print('Result is: ', result)



