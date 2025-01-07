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

def set_val(val , nst, vdict):
    if val in vdict:
        vdict[val] += nst
    else:
        vdict[val] = nst

def main(args , **kwargs):
    nblink = 75
    mult = 2024

    stones = {}
    for line in args:
        for ston in [int(s) for s in line.split()]:
            stones[ston] = 1

    for b in range(nblink):
        nstones = {}
        for st, nst in stones.items():
            slen =len(str(st)) 
            if st == 0:
                set_val(1,nst, nstones)
            elif slen %2  == 1:
                set_val(st*mult,nst, nstones)
            else:
                set_val(int(str(st)[:(slen//2)]),nst, nstones)
                set_val(int(str(st)[slen//2:]) ,nst, nstones)
        if b == 24:
            result1 = sum(nstones.values()) 
        stones = nstones
    print('Result part 1:', result1 )
    return sum(stones.values())

if __name__ == "__main__":
    stringlist ="""125 17
"""

    lines = [line.strip() for line in stringlist.strip().split('\n')]
    #assert main(lines) == 55312

    file = "input11.txt"
    with open(file,'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    result = main(lines)
    print('Result is: ', result)

