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

class BeamPos(object):

    def __init__(self,coord, direction):
        self.coord = coord
        self.dir = direction

    def __eq__(self, other):
        return (self.coord, self.dir) == (other.coord, other.dir)

    def __str__(self):
        outputstr = 'Coord: ' + str(self.coord) + '\n'
        outputstr += 'Dir: ' + str(self.dir) + '\n'
        return outputstr

class Beam(object):
    def __init__(self, startbeampos):
        self.poslist = [startbeampos]
        self.alive = True

    def eval_status(self,hdim,vdim):
        if (self.poslist[-1].coord[0] > vdim or self.poslist[-1].coord[1] > hdim
           or self.poslist[-1].coord[0] < 0 or self.poslist[-1].coord[1] < 0):
            self.alive = False
            return False

        for index, pos in enumerate(self.poslist[:-1]):
            if pos in self.poslist[index+1:]:
                self.alive = False
                return False
        return True

    def __str__(self):
        outputstr = 'Poslist: ' + str([str(pos) for pos in self.poslist]) + '\n'
        outputstr += 'Alive: ' + str(self.alive) + '\n'
        return outputstr

class Bmap(object):

    def __init__(self, bmap, startcoord = [0,-1], startdir = 'R'):

        self.bmap= bmap
        self.vdim = len(bmap)
        self.hdim = len(bmap[0])
        self.energized = [list(bm) for bm in self.bmap]
        self.cnt_e = 0
        self.beamlist = [Beam(BeamPos( startcoord, startdir))]
        self.loop()
                      
    def loop(self):
        while  len([beam for beam in self.beamlist if beam.alive]) >= 1:
            for beam in self.beamlist:
                if beam.alive:
                    self.set_next(beam)
                    beam.eval_status(self.hdim , self.vdim)
                    #print(len([beam for beam in self.beamlist if beam.alive]))

    def set_next(self, beam):
        beampos = beam.poslist[-1]
        if beampos.dir == 'R':
            coord = [beampos.coord[0], beampos.coord[1] +1]
        elif beampos.dir == 'L':
            coord = [beampos.coord[0], beampos.coord[1] -1]
        elif beampos.dir == 'U':
            coord = [beampos.coord[0]-1, beampos.coord[1] ]
        elif beampos.dir == 'D':
            coord = [beampos.coord[0]+1, beampos.coord[1] ]
        if 0 <= coord[0] and self.vdim > coord[0] and 0<= coord[1] and self.hdim > coord[1]:
            self.energized[coord[0]][coord[1]] = '#'
        try:
            action = self.bmap[coord[0]][coord[1]]
        except IndexError:
            action = '.'
        if action == '.':
            ndir = (beampos.dir)
        elif action == '-':
            if beampos.dir == 'R' or beampos.dir == 'L': 
                ndir = (beampos.dir)
            else:
                ndir = ('R', 'L')
        elif action == '/' and beampos.dir == 'R':
                ndir = ('U')
        elif action == '/' and beampos.dir == 'D':
                ndir = ('L')
        elif action == '/' and beampos.dir == 'L':
                ndir = ('D')
        elif action == '/' and beampos.dir == 'U':
                ndir = ('R')
        elif action == 'B' and beampos.dir == 'R':
                ndir = ('D')
        elif action == 'B' and beampos.dir == 'D':
                ndir = ('R')
        elif action == 'B' and beampos.dir == 'L':
                ndir = ('U')
        elif action == 'B' and beampos.dir == 'U':
                ndir = ('L')
        elif action == '|':
            if beampos.dir == 'R' or beampos.dir == 'L': 
                ndir =  ('U','D')
            else:
                ndir = (beampos.dir)

        for index, ndi in enumerate(ndir):
            nbp = BeamPos(coord, ndi)
            newstartbeam = True
            for be in self.beamlist:
                if nbp in be.poslist:
                    newstartbeam = False
                    beam.alive = False
            if newstartbeam and index == 0:
                beam.poslist.append(nbp)  
            if newstartbeam and index ==1:
                self.beamlist.append(Beam(nbp)  )


    def count_energized(self):
        self.cnt_e = 0
        for line in self.energized:
            self.cnt_e += line.count('#')
        return self.cnt_e

    def __str__(self):
        outputstr = 'Bmap: ' + str(self.bmap) + '\n'
        outputstr += 'Energ: ' + str(self.energized) + '\n'
        outputstr += 'Beamlist: ' + str([str(beam) for beam in self.beamlist]) + '\n'
        return outputstr

def main(*args , **kwargs):
    maplist = []
    result = 0

    for line in lines:
        line = line.replace("\\", 'B')
        maplist.append(line)

        #print(args)
        #print(line)

    vdim = len(maplist)
    hdim =len(maplist[0])
    starts = [ ((i, -1) ,'R') for i in range(vdim)]
    starts += [ ((-1, i) ,'D') for i in range(hdim)]
    starts += [ ((i, hdim) ,'L') for i in range(vdim)]
    starts += [ ((vdim, i) ,'U') for i in range(hdim)]
    maxresult = 0
    for start in starts:
        bmap = Bmap(maplist, startcoord = start[0], startdir = start[1])
        result = bmap.count_energized()
        print('result: ', result, ' at index: ' , str(start))
        if result > maxresult:
            maxresult = result
    #print(bmap)
    print('Result a: ', maxresult)

    return maxresult

if __name__ == "__main__":
    stringlist =r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
"""
    stringlist = stringlist.replace("\\", 'B')
    lines = [line for line in stringlist.strip().split('\n')]
    for line in lines:
        print(lines)
        print(len(lines))
    assert main(*stringlist) == 51

    file = "inputday16.txt"
    with open(file,'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    result = main(lines)
    print('Result is: ', result)
