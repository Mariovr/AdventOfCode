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
import re
import numpy as np
import z3
from aoc import AOC

#Two alternative solutions of day 13: one using numpy linalg.solve and one using z3.
#For a solution that uses the python decimal package that is able to do correct decimal floating point arithmetic, till a parametrized arbitrary precision see 13.py

nums = lambda s : [int(x) for x in re.findall(r'-?\d+', s)]
if len(sys.argv) > 1:
    example = open(sys.argv[1]).read().strip()
    inpa = [nums(line) for line in example.strip().split('\n\n')]
else:
    aoc = AOC(13 , 2024)
    inpa = [nums(line) for line in aoc.input.strip().split('\n\n') ]

def parts():
    offsets = [(0,0), (1,10000000000000)] #part number, pos offset
    for nr, add in offsets:
        ncost,zcost = 0,0
        for mdata in inpa:
            moves = np.array([[mdata[0] , mdata[2] ], [mdata[1] , mdata[3] ]] )
            targets = np.array([mdata[4]+ add , mdata[5]+ add ] )
            sol = np.linalg.solve(moves, targets).round(0) #round the solution to integers
            if [sol[0]*mdata[0]+sol[1]*mdata[2],sol[0]*mdata[1]+sol[1]*mdata[3]]==[*targets]: #if solution were real integers this is still valid else not
                ncost += 3*sol[0] + sol[1]
            b1 = z3.Int('b1')
            b2 = z3.Int('b2')
            eqset = z3.Solver()
            eqset.add(b1*mdata[0]+b2*mdata[2] == mdata[4] + add)
            eqset.add(b1*mdata[1]+b2*mdata[3] == mdata[5] + add)
            if eqset.check() == z3.sat:
                model = eqset.model()
                zcost += model[b1].as_long() * 3 + model[b2].as_long()
        print('Result: ' , nr + 1 , ' with numpy is: ', int(ncost))
        print('Result: ' , nr + 1 , ' with z3 is: ', int(zcost))
    return ncost,zcost

parts()
