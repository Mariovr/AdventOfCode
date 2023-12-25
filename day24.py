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
from decimal import *

def intersec(pvec1 , pvec2 , vvec1 , vvec2):
    try:
        t2 = vvec1[0]/(vvec1[1]*vvec2[0] - vvec2[1]*vvec1[0]) * (pvec2[1]-pvec1[1]-(vvec1[1]/vvec1[0]*(pvec2[0] - pvec1[0] ) ) )
        t1 = (pvec2[0] - pvec1[0]+ vvec2[0] *t2)/vvec1[0]
    except ZeroDivisionError: #parallel line
        t1 = float('inf') #so no intersection
        t2 = float('-inf')
    return (t1,t2)


def main(args , **kwargs):
    haillist = []
    result = 0
    lims = [200000000000000,400000000000000]
    #lims = [7,27]

    for line in args:
        pos,vel= line.split('@')
        pvec = [float(p) for p in pos.split(',') ]
        vvec = [float(v) for v in vel.split(',') ]
        haillist.append((pvec,vvec))

    intersect = 0 
    for index, hail in enumerate(haillist):
        for ind, hail2 in enumerate(haillist[index+1:]):
            #print('first' , hail)
            #print('second' , hail2)
            t1,t2 = intersec(hail[0] , hail2[0], hail[1],hail2[1])
            print(t1,t2)
            if t1 >= 0  and t2 >=0 :
                x = hail[1][0] * t1 + hail[0][0]
                y = hail2[1][1] * t2 + hail2[0][1]
                print('Pos cross: ' , x,y)
                if x >= lims[0] and x <= lims[1]:
                    if y >= lims[0] and y <= lims[1]:
                        intersect += 1

    print('Result is: ' , intersect)
    return intersect

if __name__ == "__main__":
    stringlist ="""19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
"""


#    lines = [line.strip() for line in stringlist.strip().split('\n')]
#    print(lines)
#    assert main(lines) == 2
#
    file = "inputday24.txt"
    with open(file,'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    result = main(lines)
    print('Result is: ', result)

