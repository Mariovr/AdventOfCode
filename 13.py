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

def get_m(ax, ay , bx,by, x , y ):
    return (x - (x-y)/(ax-ay)*ax) * 1/(bx - (bx-by)/(ax-ay)*ax)

def get_n(ax, ay , bx,by, x , y , m):
    return ((x-y) - m * (bx-by) )/ (ax-ay)

def main(args):
    offsets = [(0, 0, 100), (1, 10000000000000, 1e12)] #result number , pos offset, max values for pressing button
    machines = args.split('\n\n')
    for nr, add, nmax in offsets:
        mdata = []
        for i, machine in enumerate(machines):
            mdata.append([])
            for j, line in enumerate(machine.split('\n')):
                a, b = ( int(i) for i in re.findall(r'(\d+)', line))
                if j == 2:
                    mdata[i].append((a+ add,b+add))
                else:
                    mdata[i].append((a,b))
        ntoken = 0
        for nm , mdat in enumerate(mdata):
            ax, ay , bx,by, x , y = mdat[0][0],mdat[0][1],mdat[1][0],mdat[1][1],mdat[2][0],mdat[2][1]
            m = round(get_m(ax, ay , bx,by, x , y),4)
            n = get_n(ax, ay , bx,by, x , y, m)
            if 0 <= n < nmax and n.is_integer() and m.is_integer() and 0<= m < nmax:
                cost = 3*n + m
                ntoken += cost
        print('Result' , nr + 1 , ' is: ', ntoken)
    return ntoken

if __name__ == "__main__":
    file = "input13.txt"
    with open(file,'r') as f:
        lines = f.read().strip()
    result = main(lines)

