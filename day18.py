# This program is free software. It comes without any warranty, to the extent
# permitted by applicable law. You may use it, redistribute it and/or modify
# it, in whole or in part, provided that you do so at your own risk and do not
# hold the developers or copyright holders liable for any claim, damages, or
# other liabilities arising in connection with the software.
# 
#Developed by Mario Van Raemdonck, 2023;
#
# -*- coding: utf-8 -*-
#! /usr/bin/env python 

import os
import sys
from numpy import cumsum
import re

def write_map(trench):
    with open('trenchfile.txt' , 'w') as f:
        for line in trench:
            print(''.join(line))
            f.write(''.join(line)+ '\n')

def count_points(grid):
    result = 0
    for line in grid:
        result += line.count('-')
        result += line.count('|')
        result += line.count('F')
        result += line.count('J')
        result += line.count('L')
        result += line.count('7')
    return result

def count_boundaries(line, end):
    count = 0 
    saveF = False
    saveL = False
    for sign in line[:end]:
        if sign == '|':
            count += 1
            saveF = False
            saveL= False
        elif sign == 'F':
            count += 1
            saveF = True
            saveL = False
        elif sign == 'L':
            count += 1
            saveL = True
            saveF= False
        else:
            if sign == '7' and saveF:
                count += 1
                saveF =False
            elif sign == 'J' and saveL:
                count += 1
                saveL = False
            else:
                pass
    return count

def main(args , **kwargs):
    result = 0

    trenches = []
    for line in args:
        match = re.search(r'(\w)\s*(\d+)\s*\((#\w+)\)' , line)
        trenches.append([match.group(1), int(match.group(2)), match.group(3) ]) 

    #print(trenches)
    vert = [tren[1] if tren[0] == 'U' else -1*tren[1] for tren in trenches if tren[0] == 'U' or tren[0] == 'D']
    vert= cumsum(vert)
    maxv = max(vert)
    minv = min(vert)
    horz = [tren[1] if tren[0] == 'R' else -1*tren[1] for tren in trenches if tren[0] == 'R' or tren[0] == 'L']
    horz = cumsum(horz)
    maxh = max(horz)
    minh = min(horz)
    print (maxv, minv, maxh,minh)
    startc = [maxv,-1*minh]
    print('startc:', startc)
    grid = []
    for i in range(maxv+ (-1*minv)+1):
        grid.append( ['.'] * (maxh+(-1*minh)+1 ) )
    grid[startc[0]][startc[1]] = '#'
    savec = 'R'
    for d, s , c in trenches:
        match d:
            case 'U':
                for i in range(s):
                    if i ==0 and savec == 'L':
                        grid[startc[0]][startc[1]] = 'L'
                        savec = 'U'
                    if i ==0 and savec == 'R':
                        grid[startc[0]][startc[1]] = 'J'
                        savec = 'U'
                    startc[0] -= 1
                    grid[startc[0]][startc[1]] = '|'
            case 'D':
                for i in range(s):
                    if i ==0 and savec == 'L':
                        grid[startc[0]][startc[1]] = 'F'
                        savec = 'D'
                    if i ==0 and savec == 'R':
                        grid[startc[0]][startc[1]] = '7'
                        savec = 'D'
                    startc[0] += 1
                    grid[startc[0]][startc[1]] = '|'
            case 'R':
                for i in range(s):
                    if i ==0 and savec == 'U':
                        grid[startc[0]][startc[1]] = 'F'
                        savec = 'R'
                    if i ==0 and savec == 'D':
                        grid[startc[0]][startc[1]] = 'L'
                        savec = 'R'
                    startc[1] += 1
                    grid[startc[0]][startc[1]] = '-'
            case 'L':
                for i in range(s):
                    if i ==0 and savec == 'U':
                        grid[startc[0]][startc[1]] = '7'
                        savec = 'L'
                    if i ==0 and savec == 'D':
                        grid[startc[0]][startc[1]] = 'J'
                        savec = 'L'
                    startc[1] -= 1
                    grid[startc[0]][startc[1]] = '-'
    write_map(grid)

    #Count boundaries crossing to determine if we are inside or outside the surface.
    countsur = 0
    for ln, line in enumerate(grid):
        for index, surface in enumerate(line):
            if surface == '.':
                bounnum = count_boundaries(line,index) 
                if bounnum % 2 == 1:
                    #print('lineno: ' , ln)
                    #print('colno: ' , index)
                    #print('boundaries: ', bounnum)
                    countsur += 1

    print('countsur: ' , countsur)
    result = countsur + count_points(grid)

    return result

if __name__ == "__main__":
    stringlist ="""R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""

#    lines = [line.strip() for line in stringlist.strip().split('\n')]
#    #print(lines)
#    assert main(lines) == 62
#
    file = "inputday18.txt"
    with open(file,'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    result = main(lines)
    print('Result is: ', result)



