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


class Lmap(object):

    def __init__(self,source, destination):

        self.source = source
        self.destination = destination
        self.map = []

    def get_map(self, seed):
        #self.map.sort(key= lambda x : x[1])
        for tup in self.map:
            maxnum = tup[1] + tup[2]
            #print(seed)
            #print('tup' , tup[1])
            #print('tup', tup[2])
            if seed >= tup[1] and seed < maxnum:
                return tup[0] + seed - tup[1]

        #print('seed: ' + str(seed) + ' not found')
        return seed

    def __str__(self):
        outputstr = 'source: ' + str(self.source) + '\n'
        outputstr += 'destination: ' + str(self.destination) + '\n'
        outputstr += 'maplist: ' + str(self.map) + '\n'
        outputstr += 'cmaplist: ' + str(self.cmap) + '\n'
        outputstr += ''
        return outputstr


def main(*args , **kwargs):
    file = "inputday5.txt"
    seedlist = []
    maplist = {}
    source = ''
    osource = ''
    with open(file,'r') as f:
        for num , line in enumerate(f):
            if num == 0:
                seedlist = re.findall(r'(\d+)',line[6:])
                seedlist = [int(seed) for seed in seedlist]
                print(seedlist)
            else:
                match = re.search(r'(\w+)-to-(\w+)', line)
                if match:
                    source = match.group(1)
                    destination = match.group(2)
                    lmap = Lmap(source,destination)
                    maplist[source] = lmap
                    print(source + ' ' + destination)

                mapl = re.findall(r'(\d+)',line[:])
                mapl = [int(mapn) for mapn in mapl]
                if len(mapl) > 1:
                    maplist[source].map.append(mapl)
                    #print(maplist[source])

    minloc = 999999999999999999
    for seed in seedlist:
          for mapl in maplist.values():
              seed = mapl.get_map(seed)
          print('location: '+ str(seed))
          if seed < minloc:
              minloc = seed
              print('minloc changed: ' + str(minloc))
     

    print('minloc: ', minloc)


if __name__ == "__main__":
    main()
