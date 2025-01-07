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
        self.startpos = Position(startcoord, 'S')
        self.currentpos = Position(startcoord, 'S')
        self.oldpos = Position(startcoord, 'S')
        self.steps = 0

    def step(self):
        newcoord = self.get_next_coord(self.currentpos, self.oldpos)
        self.oldpos.coord = self.currentpos.coord
        self.oldpos.sign = self.currentpos.sign
        self.currentpos.coord = newcoord
        self.currentpos.sign = self.gmap[newcoord[0]][  newcoord[1] ]
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

    def __str__(self):
        outputstr = 'Coord: ' + str(self.coord) + '\n'
        outputstr += 'Sign: ' + str(self.sign) + '\n'
        return outputstr

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
    print(glmap)
    while glmap.currentpos.sign != 'S':
        glmap.step()


    print('numsteps : ' , glmap.steps/2)


if __name__ == "__main__":
    main()
