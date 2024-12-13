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

def test(ax, ay , bx,by, x , y , m):
    return ((x-y) - m * (bx-by) )/ (ax-ay)

def verify(ax, ay , bx,by, x , y , n, m):
    if (ax * n + bx *m == x) and (ay * n + by * m == y) :
        return True
    else:
        return False

def main(args , **kwargs):
    result = 0
    machines = args.split('\n\n')
    mdata = []
    for i, machine in enumerate(machines):
        mdata.append([])
        for line in machine.split('\n'):
            a, b = ( int(i) for i in re.findall(r'(\d+)', line))
            mdata[i].append((a,b))

    ntoken = 0
    for nm , mdat in enumerate(mdata):
        mcost, nmin, mmin = 1e9 , 0 ,0
        for m in range(101):
            n = test(mdat[0][0],mdat[0][1],mdat[1][0],mdat[1][1],mdat[2][0],mdat[2][1], m)
            if 0 <= n <101 and n.is_integer() and verify(mdat[0][0],mdat[0][1],mdat[1][0],mdat[1][1],mdat[2][0],mdat[2][1], n,m):
                cost = 3*n + m 
                if cost < mcost:
                    mcost = cost
                    nmin = n
                    mmin = m
        if nmin != 0:
            ntoken += mcost
    return ntoken

if __name__ == "__main__":
    stringlist ="""Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""

    lines = stringlist.strip()
    print(lines)
    assert main(lines) == 480

    file = "input13.txt"
    with open(file,'r') as f:
        lines = f.read().strip()
    result = main(lines)
    print('Result is: ', result)

