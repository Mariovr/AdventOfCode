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
import copy

class Universe(object):

    def __init__(self, gmap):
        self.gmap = gmap
        self.bigr = []
        self.bigc = []
        self.expand_universe()
        self.galdict = self.get_gal_dict()
        self.gnum = len(self.galdict)

    def expand_universe(self):
        self.bigr = []
        for index, line in enumerate(self.gmap):
            if '#' not in line:
                self.bigr.append(index)

        #Add columns
        clen = len(self.gmap[0])
        self.bigc= []
        for index in range(clen):
            if '#' not in [ val[index] for val in self.gmap]:
                self.bigc.append(index)


    def get_gal_dict(self):
        galdict = []
        cnt = 0
        for index, galaxies in enumerate(self.gmap):
            for col, g in enumerate(galaxies):
                if g == '#':
                    galdict.append((index,col))
                    cnt += 1
        return galdict


    def cal_dist(self, coord1 , coord2, expansion = 999999):
        if coord1[0] < coord2[0]:
            xstart = coord1[0]
            xend = coord2[0]
        else:
            xstart = coord2[0]
            xend = coord1[0]

        if coord1[1] < coord2[1]:
            ystart = coord1[1]
            yend = coord2[1]
        else:
            ystart = coord2[1]
            yend = coord1[1]

        mrow = 0
        for rn in self.bigr:
            if rn > xstart and rn < xend:
                mrow += 1

        mcol = 0
        for cn in self.bigc:
            if cn > ystart and cn < yend:
                mcol += 1

        return abs(xend - xstart) + abs(yend - ystart)+mrow* expansion + mcol*expansion 

    def write_map(self):
        with open('map.txt' , 'w') as f:
            for line in self.gmap:
                f.write(''.join(line)+ '\n')


def main(*args , **kwargs):
    file = "inputday11.txt"
    gmap= []
    with open(file,'r') as f:
         for line in f.readlines():
             gmap.append( [c for c in line.strip()] )

    universe = Universe(gmap)

    sumd = 0 
    for index, galc in enumerate(universe.galdict):
        for sindex in range(index+1, len(universe.galdict)):
            dist = universe.cal_dist(galc , universe.galdict[sindex])
            sumd += dist

    print('totdist: ' , sumd)


if __name__ == "__main__":
    main()
