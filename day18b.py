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

import re

#https://en.wikipedia.org/wiki/Pick%27s_theorem
def get_interior_points(surface , boundaryp ):
    return surface - boundaryp/2. + 1

#https://en.wikipedia.org/wiki/Shoelace_formula
def main(args , **kwargs):
    result = 0
    trenches = []
    d = {'0' : 'R' , '1': 'D' , '2': 'L' , '3':'U'}
    for line in args:
        match = re.search(r'\w\s*\d+\s*\(#(\w{5})(\w)\)' , line)
        trenches.append([d[match.group(2)], int(match.group(1) , 16 )  ])

    #print(trenches)
    startc = [0,0]
    newc = [0,0]
    surface = 0
    for d, s  in trenches:
        match d:
            case 'U':
                newc =[startc[0] , (startc[1] - s) ]
            case 'D':
                newc =[startc[0] , (startc[1] + s) ]
            case 'R':
                newc =[startc[0]+s , startc[1]  ]
            case 'L':
                newc =[startc[0]-s , startc[1]  ]
        surface += startc[0] * newc[1]
        surface -= startc[1] * newc[0]
        startc = newc

    #Normally need to connect back to start point, but as start coordinates are chosen to be zero...
    #surface += startc[0] * 0
    #surface -= startc[1] * 0
    surface /=2. #see shoelace formula.

    print('surface: ' , surface)
    result =  get_interior_points(surface, sum([tren[1] for tren in trenches] ) ) + sum([tren[1] for tren in trenches] )
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

    lines = [line.strip() for line in stringlist.strip().split('\n')]
    #print(lines)
    assert main(lines) == 952408144115

    file = "inputday18.txt"
    with open(file,'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    result = main(lines)
    print('Result is: ', result)



