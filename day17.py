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

class Hmap(object):
    def __init__(self, hmap, startpos = (0,0)  ):
        self.hmap = hmap
        self.vdim = len(hmap)
        self.hdim = len(hmap[0])
        self.startpos = Position(startpos ,0 , (0,1), 0, self.hdim, self.vdim )
        self.endpos = Position((self.vdim - 1 , self.hdim - 1), 0, (0,1), 0, self.hdim, self.vdim   )
        self.minhloss = self.go_naive_end(self.startpos, self.endpos)
        self.minhloss = 652 #upperbound of previous runs, it can be determined by either having a larger heuristic cost function (multiply a factor to the difference in coordinates with the endpoint) or reduce the searchspace of unique positions by not including the number of steps in same direction, and/or the current stepdirection for the uniqueness of a position.
        self.poslist = [self.startpos]
        self.checked = []

    def run(self):
        steps = 0
        while( len(self.poslist) ):
            spos = [( pos, self.cost(pos, self.endpos)) for pos in self.poslist ]
            extend = min(spos , key = lambda x: x[1])
            #print(npos) 
            npos = self.get_next_pos(extend[0])
            if steps % 1000 == 0:
                self.clean_death_path()
                print('Current Hloss: ', extend[0].hloss)

            for startpos in npos:
                if startpos not in self.checked and startpos not in self.poslist:
                    self.poslist.append(startpos) 
                #print(self.poslist)
            self.checked.append(extend[0])
            try:
                self.poslist.remove(extend[0])
            except ValueError:
                pass
            steps += 1
            if extend[0].coord == self.endpos.coord:
                if self.minhloss > extend[0].hloss:
                    self.minhloss = extend[0].hloss
                    print('Change in minhloss: ', self.minhloss)
                break

        return self.minhloss #only one path with posminpath = True should be left at the end

    def clean_death_path(self):
        for pos in self.poslist:
            if self.cost(pos,self.endpos) > self.minhloss:
                self.checked.append(pos)
                self.poslist.remove(pos)

    def cost(self, pos, end):
        #return pos.hloss + abs(pos.coord[0] - end.coord[0])*2 + abs(pos.coord[1] - end.coord[1])*2 #can return 652
        return pos.hloss + abs(pos.coord[0] - end.coord[0]) + abs(pos.coord[1] - end.coord[1])

    def go_naive_end(self,start, end ):
        curpos = start
        while(curpos.coord != end.coord):
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
        self.boundchecks = ((0,self.vdim-1) , (0,self.hdim-1) )

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
           if nd == 'R':
               steps.append( (self.cdir[1], self.cdir[0]) )
           elif nd == 'L':
               steps.append( (-1* self.cdir[1], -1* self.cdir[0]) )
           elif nd == 'S':
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
        #return (self.coord) == (other.coord) #faster to find good upperbound, can also add one of sdirsteps or cdir as extra, to find slightly better upperbound, but will not give correct result.
        return (self.coord, self.sdirsteps, self.cdir) == (other.coord, other.sdirsteps, other.cdir)

    def __str__(self):
        outputstr = 'Coord: ' + str(self.coord) + '\n'
        outputstr += 'Hloss: ' + str(self.hloss) + '\n'
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

    lines = [line.strip() for line in stringlist.strip().split('\n')]
    print(lines)
    assert main(lines) == 102

    file = "inputday17.txt"
    with open(file,'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    result = main(lines)
    print('Result is: ', result)

