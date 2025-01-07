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
from collections import deque
import heapq

#run with pypy
class NodeSearcher(object):
    def __init__(self,gmap, startc = (0,1), startstep=(1,0) , endc = (140,139), steps = 0):
        self.gmap = gmap
        self.endc = endc
        self.startc = startc
        self.set_start_nodes(startc,endc)
        self.steplist = []
        self.maxsteps = 0
        self.get_nodes()
        print([str(node) for node in self.nodes.values()])
        self.find_all_paths(self.nodes[startc], 0)

    def set_start_nodes(self, startc, endc):
        sn = Node(startc)
        sn.find_neighb(self.gmap,startc,endc)
        en = Node(endc)
        en.find_neighb(self.gmap,endc,startc)
        self.nodes = { sn.coord : sn , en.coord: en}

    def get_nodes(self):
        for pos in self.gmap.keys():
            if len([ it for it in [(pos[0] + 1 ,pos[1]),(pos[0] - 1 ,pos[1]),(pos[0] ,pos[1]-1),(pos[0] ,pos[1]+1)] if it in self.gmap.keys()] ) > 2:
                node = Node(pos)
                node.find_neighb(self.gmap,self.startc,self.endc)
                self.nodes[node.coord] = node

    def find_all_paths(self, startnode, psteps, checked = []):
        if startnode.coord == self.endc:
            #print('Path ended: ', psteps)
            if self.maxsteps < psteps:
                self.maxsteps = psteps
                print('New maxpath: ', psteps)
            return psteps
        checked.append(startnode)
        for coord,steps in self.nodes[startnode.coord].neighb.items():
            if self.nodes[coord] not in checked:
                nsteps  = psteps + steps
                self.steplist.append(self.find_all_paths( self.nodes[coord], nsteps, checked[:] ) )

    def get_max_path(self):
        return max(self.steplist)

class Node(object):
    def __init__(self,coord = (0,1),steps = 0):
        self.coord = coord
        self.neighb = {}#dict of coord with as value the distance
        self.steps = steps

    def find_neighb(self,gmap,startc, endc):
        next_dirs = [ step for step in [(1,0),(-1,0),(0,-1),(0,1)] if (self.coord[0] + step[0] , self.coord[1] + step[1]) in gmap.keys()]
        for step in next_dirs:
            pos = Position(self.coord , step)
            steps  = [step]
            nstep = 0
            while(len(steps) == 1):
                pos = pos.step(steps[0])
                nstep += 1
                steps = pos.get_pos_steps(gmap)
            if len(steps) > 1 or pos.coord == startc or pos.coord == endc:
                self.neighb[pos.coord] = nstep

    def __eq__(self, other):
        return (self.coord) == (other.coord) 

    def __str__(self):
        outputstr = 'Coord: ' + str(self.coord) + '\n'
        outputstr += 'Neighbours: ' + str(self.neighb) + '\n'
        return outputstr

class Position(object):
    def __init__(self, coord, step):
        self.coord= deepcopy(coord)
        self.cdir = step #reset for start
        self.ndir = ['S', 'R' , 'L'] #same path first option always progress in same direction

    def step(self, coord):
        return Position( (self.coord[0] + coord[0] , self.coord[1] + coord[1] ), coord)

    def check_good_step(self, step, gmap):
        newc = (self.coord[0] + step[0] ,  self.coord[1] + step[1] )
        if newc in gmap.keys():
            return True
        return False

    def get_pos_steps(self,gmap):
        steps = []
        for nd in self.ndir:
           if nd == 'R':
               step = (self.cdir[1], self.cdir[0])
           elif nd == 'L':
               step = (-1* self.cdir[1], -1* self.cdir[0]) 
           else: # nd == 'S':
               step = (self.cdir[0],self.cdir[1])
           if self.check_good_step(step, gmap):
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

    paths = NodeSearcher(smap, startc, step , endc)
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
#
    file = "inputday23.txt"
    with open(file,'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    result = main(lines)
    print('Result is: ', result)

