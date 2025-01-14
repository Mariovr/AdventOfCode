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
from aoc import AOC

aoc = AOC(16 , 2015)
inpa = aoc.input.strip().split('\n')

suetarget = """children: 3 cats: 7 samoyeds: 2 pomeranians: 3 akitas: 0 vizslas: 0 goldfish: 5 trees: 3 cars: 2 perfumes: 1"""
tmp = {mat[0] : mat[1] for mat in re.findall(r'(\w+):\s(\d+)', suetarget) }

for i, line in enumerate(inpa):
    sue_info = {mat[0] : mat[1] for mat in re.findall(r'(\w+):\s(\d+)', line) }
    if len([it for key , it in sue_info.items() if tmp[key] == it]) == len(sue_info.keys()):
        res1 = i+1
    elif len([it for key , it in sue_info.items() if  (key in [ 'cats','trees'] and tmp[key] < it ) or (key in ['pomeranians', 'goldfish'] and tmp[key] > it)  or (tmp[key] == it and key not in ['trees', 'pomeranians', 'goldfish', 'cats']) ]) == len(sue_info.keys()):
        res2 = i+1

print('Result 1:', res1)
print('Result 2:', res2)
