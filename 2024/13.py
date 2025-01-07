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
import re
from decimal import *
setcontext(Context(prec=60, Emax=MAX_EMAX, Emin=MIN_EMIN))

nums = lambda s : [Decimal(x) for x in re.findall(r'-?\d+', s)]

def verify(ax, ay , bx,by, x , y , n, m):
    eps = Decimal(1e-59)
    if (x-eps <= ax * n + bx *m <= x+ eps ) and (y-eps <= ay * n + by * m <=  y + eps) :
        return True
    else:
        return False

def get_m(ax, ay , bx,by, x , y ):
    return (x - (x-y)/(ax-ay)*ax) * 1/(bx - (bx-by)/(ax-ay)*ax)

def get_n(ax, ay , bx,by, x , y , m):
    return ((x-y) - m * (bx-by) )/ (ax-ay)

def main(args):
    offsets = [(0, Decimal(0)), (1, Decimal(10000000000000))] #part number , pos offset
    machines = [nums(line) for line in args.strip().split('\n\n') ]
    for nr, add in offsets:
        cost = 0
        for ax,ay,bx,by,x,y in machines:
            m = get_m(ax, ay , bx,by, x + add , y+add)
            n = get_n(ax, ay , bx,by, x +add , y+add, m)
            if verify(ax, ay,bx,by,x+add ,y+add,round(n,0) ,round(m,0) ): #to check that an integer solution was found.
                cost += 3*n + m
        print('Result' , nr + 1 , ' is: ', round(cost,0))
    return cost

if __name__ == "__main__":
    file = "input13.txt"
    with open(file,'r') as f:
        lines = f.read().strip()
    result = main(lines)

