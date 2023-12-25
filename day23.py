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

import sys
import re
from copy import deepcopy

class PathSearcher(object):
    def __init__(self,gmap, startc = (0,1), startstep=(1,0) , endc = (140,139), steps = 0):
        self.gmap = gmap
        self.endc = endc
        self.path = Path(gmap,startc,startstep,endc,steps)
        self.future_paths = []
        self.ended_paths = []
        self.maxsteps = 0
        self.evolve_path()
        self.run()

    def evolve_path(self):
        while(self.path.alive and not self.path.ended ):
            self.path.step()
        if self.path.ended:
            self.ended_paths.append(deepcopy(self.path))
            if self.path.steps > self.maxsteps:
                self.maxsteps = self.path.steps
                print('New maxsteps: ' , self.maxsteps)
        self.future_paths += self.path.splitpos
        #print(self.future_paths)

    def spawn_new_path(self):
        data = self.future_paths.pop()
        #print('Started Spawning paths at split points.')
        for step in data[1]:
            self.path = Path(self.gmap,data[0],step , self.endc, data[2], data[3])
            self.evolve_path()

    def run(self):
        while(len(self.future_paths) != 0):
            self.spawn_new_path()

    def get_max_path(self):
        return max([path.steps for path in self.ended_paths])

class Path(object):
    def __init__(self,gmap, startc = (0,1), startstep=(1,0) , endc = (140,139), steps = 0, his = set()):
        self.history = his
        self.gmap = gmap
        self.endpos = endc
        self.currentpos = Position(startc, startstep)
        self.history.add(self.currentpos.coord)
        self.steps = steps
        self.alive = True #alive
        self.ended = False
        self.splitpos = []

    def step(self):
        steps = self.currentpos.get_pos_steps(self.gmap,self.history)
        if len(steps) == 0:
            self.alive = False
            #print('Path Died at : ' , str(self.currentpos))
        elif len(steps) == 1:
            self.history.add(self.currentpos.coord)
            self.currentpos = self.currentpos.step(steps[0])
            self.steps += 1
        else:
            self.history.add(self.currentpos.coord)
            splitpos = self.currentpos.coord 
            self.currentpos = self.currentpos.step(steps[0])
            newh = deepcopy(self.history)
            newh.add(self.currentpos.coord) #trick to make sure that new paths dont take same dir at the split.
            self.splitpos.append( (splitpos, steps[1:], self.steps, newh ))#save current for other paths.
            self.steps += 1

        if self.currentpos.coord == self.endpos:
            self.ended = True
            #print('Path ended at steps: ' , self.steps)

    def __str__(self):
        outputstr = 'Ended: ' + str(self.ended) + '\n'
        outputstr += 'Alive: ' + str(self.alive ) + '\n'
        outputstr += 'Currentpos: ' + str(self.currentpos) + '\n'
        outputstr += 'Endpos: ' + str(self.endpos) + '\n'
        outputstr += 'Steps: ' + str(self.steps) + '\n'
        return outputstr

class Position(object):
    def __init__(self, coord, step):
        self.coord= coord
        self.cdir = step #reset for start
        self.ndir = ['S', 'R' , 'L'] #same path first option always progress in same direction
        self.limdir = {'<' : (0,-1) , '>' : (0,1), '^' : (-1,0), 'v' : (1,0) }

    def step(self, coord):
        return Position( (self.coord[0] + coord[0] , self.coord[1] + coord[1] ), coord)

    def check_good_step(self, step, gmap,history):
        newc = (self.coord[0] + step[0] ,  self.coord[1] + step[1] )
        if newc in gmap.keys() and newc not in history:
            if gmap[newc]  in  ['<','>','^','v'] :
                if self.limdir[gmap[newc] ] != step:
                    return False
                else:
                    return True
            return True
        return False

    def get_pos_steps(self,gmap,history):
        steps = []
        for nd in self.ndir:
           if nd == 'R':
               step = (self.cdir[1], self.cdir[0])
           elif nd == 'L':
               step = (-1* self.cdir[1], -1* self.cdir[0]) 
           else: # nd == 'S':
               step = (self.cdir[0],self.cdir[1])
           if self.check_good_step(step, gmap,history):
               steps.append(step)
        return steps

    def __eq__(self, other):
        return (self.coord) == (other.coord) 

    def __str__(self):
        outputstr = 'Coord: ' + str(self.coord) + '\n'
        outputstr += 'Direction: ' + str(self.cdir) + '\n'
        return outputstr

def main(args , **kwargs):
    result = 0
    startc = (0,1)
    #endc = (22,21) #sample problem
    endc = (140,139) #Real problem 

    step = (1,0)
    smap = {}
    for ind, line in enumerate(args):
        for hind, pos in enumerate(line):
            if pos in ['.','>','<','v','^']:
                smap[(ind,hind) ] = pos
        #print(line)
    print(smap)

    paths = PathSearcher(smap, startc, step , endc)
    result = paths.get_max_path()
    return result

if __name__ == "__main__":
    stringlist ="""#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
"""
#    lines = [line.strip() for line in stringlist.strip().split('\n')]
#    print(lines)
#    assert main(lines) == 154

    file = "inputday23.txt"
    with open(file,'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    result = main(lines)
    print('Result is: ', result)

