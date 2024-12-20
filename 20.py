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
from collections import Counter, defaultdict, deque #defaultdict provides default function when accessing key not present

#Note best to run with pypy.
with open('input20.txt','r') as aoc:
    text = aoc.read()
inpa = text.strip().split('\n')
stringlist ="""###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""
#inpa = [line for line in stringlist.strip().split('\n')]
steps = [[0, 1], [1, 0], [0, -1], [-1, 0]]

def f_path(mp,sc,ec, dimx , dimy):
    d = deque([])
    nstep =0
    d.append((nstep,sc,(0,0))) #start c ,pos, cheat
    path = {}
    path[sc] = 0
    seen = set()
    seen.add(sc)
    while(d):
        ostep , sc, ch = d.popleft()
        for i, step in enumerate(steps):
            npos = (sc[0] + step[0],sc[1] + step[1])
            if 0 <= npos[0] < dimx and 0 <= npos[1] < dimy and mp[(npos[0],npos[1])] == '.': 
                nstep = ostep + 1
                if npos not in seen:
                    d.append((nstep, npos, ch))
                    seen.add(npos)
                    path[npos] = nstep
                if npos  == ec:
                    sc = npos
                    break
        if sc == ec:
            break
    return path, nstep

def parts():
    dimx, dimy = len(inpa), len(inpa[0])
    print('dims(x,y):' , dimx ,dimy)
    mp = {}
    sc, ec =(0,0) , (0,0)
    pl = []
    for i, line in enumerate(inpa):
        for  j, l in enumerate(list(line)):
            mp[(i,j)] = l
            if l == 'S':
                sc = (i,j)
                mp[(i,j)] = '.'
            if l =='E':
                ec = (i,j)
                mp[(i,j)] = '.'
            if 0 < i < dimx -1 and 0 < j < dimy -1 and l in ('.' , 'E', 'S'):
                pl.append((i,j))
    print('s' , sc)
    print('e' , ec)
    opath , spl= f_path(mp,sc,ec,dimx,dimy) #find the path, without using a cheat, then later that will be used to start cheats until max cheat length.
    print('start path length: ' ,spl)
    cheatll = [2,20]
    resl = []
    for cl in cheatll:
        res = 0
        chl = defaultdict(set) #dictionary that maps the number of steps save by a cheat, onto the unique cheats in a set
        for i, (w1,w2) in enumerate([p for p in opath.keys()]):
            chs = opath[w1,w2] #steps to reach cheat start
            d = deque([(0,w1,w2)]) #chstep , px , py
            seen = set()
            while(d):
                stepsc , x,y = d.popleft()
                for ns, (dx,dy) in enumerate(steps):
                    npx = x + dx
                    npy = y + dy
                    nsc = stepsc + 1
                    if 0 <= npx < dimx  and 0 <= npy < dimy and (npx,npy) not in seen:
                        seen.add((npx,npy))
                        if nsc < cl: #check that #cheatsteps is lower then the limit, only then do a next
                            d.append((nsc,npx,npy))
                        if (npx,npy) in pl: #if end position of the cheat is back on the path, check if the cheat reduced the stepcount.
                            nstep = opath[ (npx,npy)] #total path steps when using cheat is: steps to reach startpos of cheat + steps cheat + (path length - steps to reach end from cheat end)
                            if (spl - nstep) + chs + nsc < spl:  #cheat saved steps
                                chl[nstep - nsc - chs].add((w1,w2, npx,npy))
                                if nstep-nsc-chs >= 100:
                                    res +=1
            if i % 1000 == 0:
                print('it:' , i , 'res: ' , res)
        resl.append(res)
        print('Result for cheat length: ' , cl , ' is: ' , res)
        #for k , v in chl.items(): #for debugging purposes prints the number of steps saved, together with the number of cheats that allows to save that number of steps.
            #print('dif: ' , k , 'num cheats: ' , len(v))
    return resl[0] , resl[1]

result1,result2 = parts()
print('Result 1:', result1)
print('Result 2:', result2)

