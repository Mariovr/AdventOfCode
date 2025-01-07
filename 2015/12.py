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
sys.setrecursionlimit(99999999)
import re
from aoc import AOC

aoc = AOC(12 , 2015)
struct = eval(aoc.input)

nums = lambda s : [int(x) for x in re.findall(r'-?\d+', s)] #helper for part 1

def add_v_nums(e): #helper for part 2
    nlist = []
    if isinstance(e, list):
        for a in e:
            nlist += add_v_nums(a)

    elif isinstance(e,dict):
        for key in e .keys():
            if 'red' == e[key]:
                return [0]
            else:
                nlist += add_v_nums(e[key] )
    else:
        nlist += [e]
    return nlist

print('Result 1:', sum(nums(aoc.input)) )
print('Result 2:', sum([i for i in add_v_nums(struct) if isinstance(i,int)] ))
