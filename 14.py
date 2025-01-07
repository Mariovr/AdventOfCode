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

from collections import Counter, defaultdict, deque
import re

def main(args , **kwargs):
    dimx = 101
    dimy = 103
    time = 100
    cx = dimx//2
    cy = dimy//2
    plist = []
    q1,q2,q3,q4 = 0,0,0,0
    for i, line in enumerate(args):
        x,y,vx,vy = (map(int, re.findall('-?\d+',line)) )
        plist.append((x,y,vx,vy))
        nx = (x + vx * time) %dimx
        ny = (y + vy * time) %dimy
        if nx < cx and ny < cy:
            q1 += 1
        if nx < cx and ny > cy:
            q2 += 1
        if nx > cx and ny < cy:
            q3 += 1
        if nx > cx and ny > cy:
            q4 += 1
    print('Result1 is: ', q1 * q2 * q3 *q4 )

    for t in range(0,100000):
        if t % 100 ==0:
            print('#for time t:', t)
        nplist = []
        for (x,y,vx,vy) in plist:
            nplist.append(((x + vx * t) %dimx,(y + vy * t) %dimy  ))
        #search tree trunk
        checked = set()
        for x,y in nplist:
            ttsz = 0
            if (x,y) not in checked: 
                d = deque([(x,y)])
                while d:
                    x, y = d.popleft()
                    ttsz += 1
                    checked.add((x,y))
                    nx = x + 1
                    if 0<= nx < dimx and (nx,y) in nplist and (nx,y) not in checked:
                          d.append((nx,y))
                    nx = x - 1
                    if 0<= nx < dimx and (nx,y) in nplist and (nx,y) not in checked:
                          d.append((nx,y))
                #should be a line of at least 10 for the trunk
                if ttsz > 10:
                    print('#for time t:', t, 'ttsz : ' , ttsz)
                    dmap=[['.' for i in range(dimy)] for j in range( dimx)]
                    for (x,y) in nplist:
                        dmap[x][y] = 'X'
                    for line in dmap:
                        print(''.join(line) )
                    break
        if ttsz > 10:
            break

    return t

if __name__ == "__main__":
    stringlist ="""p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""

    lines = [line.strip() for line in stringlist.strip().split('\n')]
    print(lines)
    #assert main(lines) == 12

    file = "input14.txt"
    with open(file,'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    result = main(lines)
    print('Result2 is: ', result)
