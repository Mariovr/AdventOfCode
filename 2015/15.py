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
sys.setrecursionlimit(1<<30)
import re
from aoc import AOC

if len(sys.argv) > 1:
    example = open(sys.argv[1]).read().strip()
    inpa = [line.strip() for line in example.strip().split('\n')]
else:
    aoc = AOC(15 , 2015)
    inpa = aoc.input.strip().split('\n')

nums = lambda s : [int(x) for x in re.findall(r'-?\d+', s)]

ingr_l = []
for line in inpa:
    ingr_l.append(nums(line))

def get_coefset(target_t , numc):
    if numc == 1:
        yield (target_t,)
    else:
        for j in range(target_t+1):
            for coefs in get_coefset(target_t - j,numc -1 ):
                yield (j,) + coefs

target_t = 100
res1,res2,total = 0,0,0
for coefs in get_coefset(target_t , len(ingr_l) ):
    total = 1
    t_calories = sum([c*ingr[-1] for c,ingr in zip(coefs,ingr_l)])
    for i in range(4):
        t_prop = sum([c*ingr[i] for c,ingr in zip(coefs,ingr_l)])
        if t_prop < 0:
            total = 0
        else:
            total *= t_prop 
    if total > res1:
        res1 = total
    if total > res2 and t_calories == 500:
        res2 = total

print('Result 1:', res1)
print('Result 2:', res2)
