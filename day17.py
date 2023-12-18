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
import numpy as np
import re

class Hmap(object):
    def __init__(self, hmap, startpos = (0,0)  ):
        self.hmap = hmap
        self.vdim = len(hmap)
        self.hdim = len(hmap[0])
        self.startpos = Position(startpos ,0 , (0,1), 0, self.hdim, self.vdim )
        self.endpos = Position((self.vdim - 1 , self.hdim - 1), 0, (0,1), 0, self.hdim, self.vdim   )
        self.minhloss = 0
        self.poslist = [self.startpos]
        self.checked = []

    def run(self):
        steps = 0
        while(True ):
            npos = []
            for index, cpos in enumerate(self.poslist):
                #print(cpos)
                npos += [(index, pos, self.cost(pos, self.endpos)) for pos in  self.get_next_pos(cpos)]
                #print (npos)

            extend = min(npos , key = lambda x: x[2])
            if steps % 1000 == 0:
                print(extend[2])
            for startpos in [pos[1] for pos in npos if pos[0] == extend[0]]:
                if startpos not in self.checked and self.poslist.count(startpos) < 4:
                    self.poslist.append(startpos) 
                #print(self.poslist)

            self.checked.append(self.poslist[extend[0]] )
            del self.poslist[extend[0]]
            steps += 1
            if extend[1] == self.endpos:
                break

        return extend[1].hloss #only one path with posminpath = True should be left at the end

    def cost(self, pos, end):
        return pos.hloss + abs(pos.coord[0] - end.coord[0]) + abs(pos.coord[1] - end.coord[1])

    def go_naive_end(self,start, end ):
        curpos = start
        while(curpos != end):
            steps = curpos.get_pos_steps()
            curpos = curpos.step(steps[0], self.hmap)
        return curpos.hloss

    def get_next_pos(self,cpos):
        steps = cpos.get_pos_steps()
        pos = []
        for step in steps:
            pos.append(cpos.step(step, self.hmap))
        return pos

    def __str__(self):
        outputstr = 'Hmap: ' + str(self.hmap) + '\n'
        return outputstr

class Position(object):
    def __init__(self, coord, hloss, step, sdirsteps, hdim, vdim):
        self.coord= coord
        self.hloss = hloss #tot heatloss related to contained path
        self.sdirsteps = sdirsteps
        self.cdir = step #reset for start
        self.ndir = ['S', 'R' , 'L'] #same path first option always progress in same direction
        self.hdim = hdim
        self.vdim = vdim
        self.boundchecks = [(0,self.vdim-1) , (0,self.hdim-1) ]

    def step(self, coord, hmap):
        newc0 = self.coord[0] + coord[0] 
        newc1 = self.coord[1] + coord[1] 
        if coord == self.cdir:
            sdirs = self.sdirsteps + 1
        else:
            sdirs = 1
        assert sdirs <= 3
        return Position( (self.coord[0] + coord[0] , self.coord[1] + coord[1] ), self.hloss + hmap[newc0][newc1] , coord, sdirs, self.hdim, self.vdim)

    def get_pos_steps(self):
        steps = []
        for nd in self.ndir:
           match nd:
               case 'R':
                   steps.append( (self.cdir[1], self.cdir[0]) )
               case 'L':
                   steps.append( (-1* self.cdir[1], -1* self.cdir[0]) )
               case 'S':
                   if self.sdirsteps < 3: 
                       steps.append( (self.cdir[0],self.cdir[1]) )

        if self.coord[0] in self.boundchecks[0]:
            for index, step in enumerate(steps):
                if self.coord[0] + step[0] == self.vdim or self.coord[0]+ step[0] < 0:
                    del steps[index]

        if self.coord[1] in self.boundchecks[1]:
            for index, step in enumerate(steps):
                if self.coord[1] + step[1] == self.hdim or self.coord[1] +step[1] <  0:
                    del steps[index]
        return steps


    def __eq__(self, other):
        return (self.coord) == (other.coord)

    def __str__(self):
        outputstr = 'Coord: ' + str(self.coord) + '\n'
        outputstr += 'Hloss: ' + str(self.hloss) + '\n'
        ##outputstr += 'ShortestFound: ' + str(self.sfound) + '\n'
        return outputstr

def main(args , **kwargs):
    maplist = []
    result = 0

    for line in args:
        maplist.append([int(i) for i in line])
        print(line)

    startpos = (0,0)
    hmap = Hmap(maplist, startpos = startpos)
    result = hmap.run()
    print('Result is: ' , result)
    
    return result

if __name__ == "__main__":
    stringlist ="""2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""

#    lines = [line.strip() for line in stringlist.strip().split('\n')]
#    print(lines)
#    assert main(lines) == 102
#
    file = "inputday17.txt"
    with open(file,'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    result = main(lines)
    print('Result is: ', result)

