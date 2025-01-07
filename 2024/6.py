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

def main1(dmap,startp,  step , stepl):
    pos = startp
    npos = startp
    nstep = step
    savepd = set()
    vpos = 0
    while(npos[0] >= 0 and npos[0] < len(dmap) and npos[1] >= 0 and npos[1] <len(dmap[0]) ):
        if dmap[npos[0]][npos[1]] == '#':
            nstep = (nstep + 1)%4
        else:
            if dmap[npos[0]][npos[1]] != 'X':
                dmap[npos[0]][npos[1]] = 'X'
                vpos += 1
            pos = npos
            if (npos[0], npos[1] , nstep) not in savepd:
                savepd.add((npos[0] , npos[1] , nstep))
            else:
                vpos = -1
                break
        npos = (pos[0] + stepl[nstep][0] , pos[1] + stepl[nstep][1])
    return vpos

def write_map(dmap):
    with open('map.txt','w') as f:
        for line in dmap:
            f.write(''.join(line) + '\n')

def main(args, **kwdmap):
    result = 0
    stepl = [(-1,0), (0,1),(1,0),(0,-1) ]
    dmap = []
    for i, line in enumerate(args):
        dmap.append(list(line)  )
        j = line.find('^') 
        if j >0:
            startp = (i,j)

    vpos = main1(dmap, startp , 0 , stepl)
    write_map(dmap)
    print('Result 1: ' , vpos)

    pos = startp
    npos = startp 
    nstep = 0
    obstset = set()
    while(npos[0] >= 0 and npos[0] < len(dmap) and npos[1] >= 0 and npos[1] <len(dmap[0]) ):
        if dmap[npos[0]][npos[1]] == '#':
            nstep = (nstep + 1) %4
        else:
            dmap[npos[0]][npos[1]] = '#'
            #returns -1 in case of loop.
            if main1(dmap, startp , 0 ,stepl) == -1:
                obstset.add(npos)
            dmap[npos[0]][npos[1]] = '.'
            pos = npos
        npos = (pos[0] + stepl[nstep][0] , pos[1] + stepl[nstep][1])
    return len(obstset)


if __name__ == "__main__":
    stringlist ="""....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

    lines = [line.strip() for line in stringlist.strip().split('\n')]
    print(lines)
    assert main(lines) == 6

    file = "input6.txt"
    with open(file,'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    result = main(lines)
    print('Result 2 is: ', result)

