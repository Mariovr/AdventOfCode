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
        self.minhloss = 800  #upperbound due to previous bad run
        self.poslist = [self.startpos]
        self.checked = []

    def run(self):
        steps = 0
        while( len(self.poslist) ):
            spos = [( pos, self.cost(pos, self.endpos)) for pos in self.poslist ]
            extend = min(spos , key = lambda x: x[1])
            npos = self.get_next_pos(extend[0])

            if steps % 300 == 0:
                test = pos.hloss + abs(pos.coord[0] - self.endpos.coord[0])*6 + abs(pos.coord[1] - self.endpos.coord[1])*6 #
                if test < self.minhloss:
                    self.minhloss = test
                self.clean_death_path()
                print('Naieve End: ', self.minhloss)
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

        return self.minhloss 

    def clean_death_path(self):
        for pos in self.poslist:
            if self.cost(pos,self.endpos) > self.minhloss:
                self.checked.append(pos)
                self.poslist.remove(pos)

    def cost(self, pos, end):
        return pos.hloss + abs(pos.coord[0] - end.coord[0]) + abs(pos.coord[1] - end.coord[1]) #increase mult factor of cost function to get faster first guesses, but the higher cost the higher risk on deviations from answer.
        #return pos.hloss 

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
    def __init__(self, coord, hloss, step, sdirsteps, hdim, vdim, maxstepssd = 10, minstepsd = 4):
        self.coord= coord
        self.hloss = hloss #tot heatloss related to contained path
        self.sdirsteps = sdirsteps
        self.cdir = step #reset for start
        self.ndir = ['S', 'R' , 'L'] #same path first option always progress in same direction
        self.hdim = hdim
        self.vdim = vdim
        self.boundchecks = [(0,1,2,3,self.vdim-2,self.vdim-3,self.vdim-4,self.vdim-1) , (0,1,2,3,self.hdim-2,self.hdim-4,self.hdim-3,self.hdim-1) ]
        self.maxstepssd = maxstepssd
        self.minstepsd = minstepsd

    def step(self, coord, hmap):
        newc0 = self.coord[0] + coord[0] 
        newc1 = self.coord[1] + coord[1] 
        if coord == self.cdir:
            sdirs = self.sdirsteps + 1
        else:
            sdirs = 1
        assert sdirs <= self.maxstepssd
        return Position( (newc0 , newc1 ), self.hloss + hmap[newc0][newc1] , coord, sdirs, self.hdim, self.vdim)

    def get_pos_steps(self):
        steps = []
        if self.sdirsteps >= self.minstepsd:
            boundchecksteps = 1
        else:
            boundchecksteps = (self.minstepsd-self.sdirsteps)

        for nd in self.ndir:
           add = True

           if nd == 'R':
                   if self.sdirsteps >= self.minstepsd: #switch of dir is allowed 
                       step = (self.cdir[1], self.cdir[0])
                       if self.coord[0] in self.boundchecks[0]:
                           if self.coord[0] + step[0]*(self.minstepsd-1) >= self.vdim or self.coord[0]+ step[0]*(self.minstepsd-1) < 0:
                              add = False
                       if self.coord[1] in self.boundchecks[1]:
                           if self.coord[1] + step[1]*(self.minstepsd-1) >= self.hdim or self.coord[1] +step[1] * (self.minstepsd-1) <  0:
                              add = False
                       if add:
                           steps.append(  step )
           elif nd == 'L':
                   if self.sdirsteps >= self.minstepsd: #switch of dir is allowed 
                       step = (-1* self.cdir[1], -1* self.cdir[0])
                       if self.coord[0] in self.boundchecks[0]:
                           if self.coord[0] + step[0]*(self.minstepsd-1)>= self.vdim or self.coord[0]+ step[0]*(self.minstepsd-1)< 0:
                              add = False
                       if self.coord[1] in self.boundchecks[1]:
                           if self.coord[1] + step[1]* (self.minstepsd-1)>= self.hdim or self.coord[1] +step[1] * (self.minstepsd-1)<  0:
                              add = False
                       if add:
                           steps.append(  step )
           elif nd == 'S':
                   if self.sdirsteps < self.maxstepssd: 
                       step = (self.cdir[0],self.cdir[1])
                       if self.coord[0] in self.boundchecks[0]:
                           if self.coord[0] + step[0]*boundchecksteps >= self.vdim or self.coord[0]+ step[0]*boundchecksteps < 0:
                              add = False
                       if self.coord[1] in self.boundchecks[1]:
                           if self.coord[1] + step[1]* boundchecksteps >= self.hdim or self.coord[1] +step[1] * boundchecksteps <  0:
                              add = False
                       if add:
                           steps.append(  step )

        return steps


    def __eq__(self, other):
        #return (self.coord,  self.cdir) == (other.coord, other.cdir) #to get a good first guess to set minhloss
        return (self.coord, self.sdirsteps, self.cdir) == (other.coord, other.sdirsteps, other.cdir)

    def __str__(self):
        outputstr = 'Coord: ' + str(self.coord) + '\n'
        outputstr += 'Hloss: ' + str(self.hloss) + '\n'
        outputstr += 'sdirsteps: ' + str(self.sdirsteps) + '\n'
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
    assert main(lines) ==  94

    file = "inputday17.txt"
    with open(file,'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    result = main(lines)
    print('Result is: ', result)

