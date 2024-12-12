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
from collections import deque

def main(args , **kwargs):
    result = 0
    result1 = 0
    dimx = len(args)
    dimy = len(args[0])
    slist = deque([]) 
    steps = [[-1, 0], [1, 0], [0, -1], [0, 1]]
    dmap = {}
    for i, line in enumerate(args):
        for  j, l in enumerate(list(line)):
            dmap[(i,j)] = l
    seen = set()
    for i, line in enumerate(args):
        for  j, l in enumerate(list(line)):
            if (i,j) not in seen:
                area = 0
                tsurf = 0
                nsurf = 0
                slist.append((i,j))
                #print('start:' , i , j)
                surfl = set()
                while slist:
                    x , y = slist.pop()
                    seen.add((x,y) )
                    area += 1
                    for sx , sy in steps:
                        xx = x + sx
                        yy = y + sy
                        if  0<= xx < dimx and 0 <= yy < dimy and (xx,yy) not in seen and l == dmap[(xx,yy)] :
                            slist.append((xx,yy))
                            seen.add((xx,yy) )

                        if not (0<= xx < dimx) or not (0 <= yy < dimy) or not (l == dmap[(xx,yy)]) and (xx,yy) :
                            cf = False
                            tx , ty = xx , yy
                            ncon = 0
                            nsurf +=1
                            for bx , by in steps:
                                if (tx+bx,ty+by,sx,sy) in surfl:
                                    cf = True
                                    ncon +=1 
                            surfl.add((xx,yy,sx,sy))
                            if not cf :
                                tsurf += 1
                            #already counted this side to much
                            if ncon > 1:
                                tsurf -= 1
                            #print('tsurf:' , x , y, tsurf)

                #print('are surf:' , area , tsurf)
                result += area * tsurf
                result1 += area * nsurf

    print('Result 1: ' , result1)
    return result

if __name__ == "__main__":
    stringlist ="""RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""

    lines = [line.strip() for line in stringlist.strip().split('\n')]
    print(lines)
    assert main(lines) == 1206

    file = "input12.txt"
    with open(file,'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    result = main(lines)
    print('Result 2 is: ', result)

