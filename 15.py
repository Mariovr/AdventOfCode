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
from collections import Counter, defaultdict, deque
import re
from aoc import AOC

aoc = AOC(15 , 2024)
input = aoc.input.strip().split('\n\n')
stringlist ="""##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""
#stringlist ="""#######
##...#.#
##.....#
##..OO@#
##..O..#
##.....#
########
#
#<vv<<^^<<^^
#"""
#input = [line.strip() for line in stringlist.strip().split('\n\n')]
#print(input)

steps = [[0, 1], [1, 0], [0, -1], [-1, 0]]

def part1():
    inpm, inpa = input[0].split('\n'), ''.join(input[1].split('\n'))
    stepd = { '>': [0, 1], 'v': [1, 0], '<': [0, -1], '^': [-1, 0]}
    dimx, dimy = len(inpm),  len(inpm[0])
    print('dims:' , dimx ,dimy)
    mp = {}
    sc = (0,0)
    for i, line in enumerate(inpm):
        for  j, l in enumerate( list(line)):
            mp[(i,j)] = l
            if l == '@':
                sc = (i,j)
                mp[(i,j)] = '.'
    nsc = (0,0)
    for i in list(inpa):
        ns = stepd[i]
        nsc = (sc[0] + ns[0] , sc[1]+ns[1])
        if mp[nsc] == '.':
            sc = nsc
        elif mp[nsc] == '#':
            continue
        else:
            d = deque([nsc])
            while(d):
                o1,o2 = d.pop()
                no1,no2 = o1 + ns[0],  o2 + ns[1]
                if mp[(no1,no2)] == 'O':
                    d.append((no1,no2))
                elif mp[(no1,no2)] == '#':
                    continue
                else:
                    mp[(no1,no2)] = 'O' 
                    mp[nsc] = '.' 
                    sc = nsc
    res = 0
    for i in range(dimx):
        for j in range(dimy):
            if mp[(i,j)] == 'O':
                res += 100 * i + j 

    return res


def part2():
    res = 0
    inpm, inpa = input[0].split('\n'), input[1].strip()
    stepd = { '>': [0, 1], 'v': [1, 0], '<': [0, -1], '^': [-1, 0]}
    dimx = len(inpm)
    dimy = len(inpm[0])*2
    print('dims:' , dimx ,dimy)
    mp = {}
    sc = (0,0)
    for i, line in enumerate(inpm):
        for  j, l in enumerate( list(line)):
            if l == '#' or l == '.':
                mp[(i,j*2)] = l
                mp[(i,j*2+1)] = l
            elif l == 'O':
                mp[(i,j*2)] = '1'
                mp[(i,j*2+1)] = '2'
            elif l == '@':
                sc = (i,j*2)
                mp[(i,j*2)] = '.'
                mp[(i,j*2+1)] = '.'
    print('startc:' , sc)
    pm = ''
    for i in range(dimx):
        for j in range(dimy):
            pm += mp[(i,j)]
        pm += '\n'
    print(pm)

    nsc = (0,0)
    inpaa = ''
    for a in inpa.split('\n'):
        inpaa += str(a)
    #print(list(inpaa))
    for ind, i in enumerate(list(inpaa)):
        ns = stepd[i]
        nsc = (sc[0] + ns[0] , sc[1]+ns[1])
        if mp[nsc] == '.':
            sc = nsc
        elif mp[nsc] == '#':
            continue
        else:
            pc = {}
            if i == '<' or i =='>':
                d = deque([nsc])
                while(d):
                    o1,o2 = d.pop()
                    no1 = o1 + ns[0]*2
                    no2 = o2 + ns[1]*2
                    if mp[(no1,no2)] == '1' or mp[(no1,no2)] == '2':
                        pc[(no1,no2)] = mp[(no1,no2 -ns[1])]
                        pc[(no1,no2-ns[1])] = mp[(no1,no2 -2*ns[1])]
                        d.append((no1,no2))
                    elif mp[(no1,no2)] == '#':
                        continue
                    else:
                        mp[(no1,no2)] = mp[(no1,no2 -ns[1])] 
                        mp[(no1,no2-ns[1])] = mp[(no1,no2 -2*ns[1])]
                        for c in pc:
                            mp[c] = pc[c]
                        mp[nsc] = '.'
                        sc = nsc
            else:
                #position on start of box
                if mp[nsc] == '1':
                    d = deque([nsc])
                elif mp[nsc] == '2':
                    d = deque([(nsc[0] , nsc[1] - 1)])
                else:
                    print('cant come here')
                    sys.exit(1)
                move = True
                dots = []
                while(d):
                    o1, o2 = d.popleft()
                    no1 = o1 + ns[0]
                    no2 = o2 + ns[1]
                    if mp[(no1,no2)] == '#' or mp[(no1,no2+1)] == '#' :
                        move = False
                        break
                    elif mp[(no1,no2)] == '.':
                        if mp[(no1,no2 + 1)] == '.':
                            pc[(no1,no2)] = '1'
                            pc[(no1,no2+1)] = '2'
                            continue
                        elif mp[(no1,no2 + 1)] == '1':
                            pc[(no1,no2)] = '1'
                            pc[(no1,no2+1)] = '2'
                            d.append((no1,no2+1))
                            if (no1,no2+2) not in pc :
                                dots.append((no1,no2+2) )
                        else:
                            move = False
                            break
                    elif mp[(no1,no2)] == '1':
                        d.append((no1,no2))
                    elif mp[(no1,no2)] == '2':
                        pc[(no1,no2)] = '1'
                        if (no1,no2-1) not in pc  :
                            dots.append((no1,no2-1) )
                        d.append((no1,no2-1))
                        if mp[(no1,no2+1)] =='.':
                            pc[(no1,no2+1)] = '2'
                        elif mp[(no1,no2+1)] =='1':
                            pc[(no1,no2+1)] = '2'
                            if (no1,no2+2) not in pc:
                                dots.append((no1,no2+2) )
                            d.append((no1,no2+1))
                        else:
                            move = False
                            break
                if move:
                    for c in pc:
                        mp[c] = pc[c]
                    for dc in dots:
                        if dc not in pc:
                            mp[dc] = '.'
                    if mp[nsc] == '1':
                        mp[(nsc[0] , nsc[1] +1)] = '.'
                    elif mp[nsc] == '2':
                        mp[(nsc[0] , nsc[1] -1)] = '.'
                    mp[nsc] = '.' 
                    sc = nsc

#        if 0 < ind < 40:
#            print('after move:' , i)
#            mp[sc] = '@'
#            pm = ''
#            for i in range(dimx):
#                for j in range(dimy):
#                    pm += mp[(i,j)]
#                pm += '\n'
#            mp[sc] = '.'
#            print(pm)
#
    for i in range(dimx):
        for j in range(dimy):
            if mp[(i,j)] == '1':
                res += 100 * i + j 

    return res

result1 = part1()
result2 = part2()
# Submit
print('Result 1:', result1)
#aoc.submit(1, result1)
print('Result 2:', result2)
#aoc.submit(2, result2)

