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
import re
from functools import reduce
import numpy as np

class Gmap(object):

    def __init__(self, gmap, startcoord):
        self.gmap = gmap
        self.dgmap = [l.copy() for l in gmap ]
        self.startpos = Position(startcoord, 'S')
        self.currentpos = Position(startcoord, 'S')
        self.oldpos = Position(startcoord, 'S')
        self.steps = 0
        self.path = []

    def step(self ):
        self.path.append(self.currentpos.copy())
        newcoord = self.get_next_coord(self.currentpos, self.oldpos)
        self.oldpos.coord = self.currentpos.coord
        self.oldpos.sign = self.currentpos.sign
        self.currentpos.coord = newcoord
        self.currentpos.sign = self.gmap[newcoord[0]][  newcoord[1] ]
        self.dgmap[self.oldpos.coord[0]][self.oldpos.coord[1] ] = 'X'
        self.steps += 1

    def get_next_coord(self, newpos, oldpos, nextstep = (0,1)):
        match newpos.sign:
            case 'F':
                newc = ( ( newpos.coord[0] , newpos.coord[1] + 1), (newpos.coord[0]+1 , newpos.coord[1] ) )
            case '-':
                newc = ( ( newpos.coord[0] , newpos.coord[1] + 1), (newpos.coord[0] , newpos.coord[1]-1 ) )
            case '|':
                newc = ( ( newpos.coord[0]+1 , newpos.coord[1] ), (newpos.coord[0]-1 , newpos.coord[1] ) )
            case '7':
                newc = ( ( newpos.coord[0]+1 , newpos.coord[1] ), (newpos.coord[0] ,newpos.coord[1]-1  ) )
            case 'L':
                newc = ( ( newpos.coord[0]-1 , newpos.coord[1] ), (newpos.coord[0] , newpos.coord[1]+1 ) )
            case 'J':
                newc = ( (newpos.coord[0]-1 , newpos.coord[1] ), (newpos.coord[0] , newpos.coord[1]-1 ) )
            case 'S':
                print('We are at start position so we use the nextstep addition')
                return (newpos.coord[0] + nextstep[0]  , newpos.coord[1] + nextstep[1]  )

        if newc[0] == oldpos.coord:
            return newc[1]
        else:
            return newc[0]

    def __str__(self):
        outputstr = 'start pos: ' + str(self.startpos) + '\n'
        outputstr += 'Current position: ' + str(self.currentpos) + '\n'
        outputstr += 'Old position: ' + str(self.oldpos) + '\n'
        outputstr += 'Steps: ' + str(self.steps) + '\n'
        return outputstr


class Position(object):

    def __init__(self, coord, sign):
        self.coord= coord
        self.sign = sign

    def copy(self):
        return type(self)(self.coord, self.sign)

    def __str__(self):
        outputstr = 'Coord: ' + str(self.coord) + '\n'
        outputstr += 'Sign: ' + str(self.sign) + '\n'
        return outputstr


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

def main(*args , **kwargs):
    file = "inputday10.txt"
    gmap= []

    with open(file,'r') as f:
        for index, line in enumerate(f.readlines()):
           gmap.append([c for c in line.strip()])
           match = re.search(r'S',line)
           if match != None:
               startpos = (index , match.start() )

    print('startpos: ' , startpos, ' contains: ' , gmap[startpos[0]][startpos[1]])
    glmap = Gmap(gmap, startpos)
    glmap.step()
    while glmap.currentpos.sign != 'S':
        glmap.step()

    print('numsteps : ' , glmap.steps/2)

    dmap = []
    #create the surfaces as .
    for line in glmap.dgmap:
        dmap.append(['.' if char != 'X' else char for char in line ])

    #put back the original signs
    for pos in glmap.path:
        dmap[pos.coord[0]][pos.coord[1]] = pos.sign

    #Count boundaries crossing to determine if we are inside or outside the surface.
    countsur = 0
    for ln, line in enumerate(dmap):
        for index, surface in enumerate(line):
            if surface == '.':
                bounnum = count_boundaries(line,index) 
                if bounnum % 2 == 1:
                    #print('lineno: ' , ln)
                    #print('colno: ' , index)
                    #print('boundaries: ', bounnum)
                    countsur += 1


    #Gives a nice depiction of the path without noise.
    with open('pathfile.txt' , 'w') as f:
        for line in dmap:
            print(''.join(line))
            f.write(''.join(line)+ '\n')

    print('Contained surfaces: ', countsur)

if __name__ == "__main__":
    main()
