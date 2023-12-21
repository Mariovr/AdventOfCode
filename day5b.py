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

import re

class Lmap(object):

    def __init__(self,source, destination):

        self.source = source
        self.destination = destination
        self.map = []

    def get_map(self, seed):
        for tup in self.map:
            maxnum = tup[1] + tup[2]
            if seed >= tup[1] and seed < maxnum:
                return tup[0] + seed - tup[1]

        #print('seed: ' + str(seed) + ' not found')
        return seed

    def get_index(self,loc):
        for tup in self.map:
            maxnum = tup[0] + tup[2]
            if loc >= tup[0] and loc < maxnum:
                return tup[1] + loc - tup[0]

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
    maplist = []
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
                    maplist.append(lmap)
                    print(source + ' ' + destination)
                    
                mapl = re.findall(r'(\d+)',line[:])
                mapl = [int(mapn) for mapn in mapl]
                if len(mapl) > 1:
                    maplist[-1].map.append(mapl)
                    #print(maplist[source])

    #Noticed that in the first slice there is already a very low location only 79 million
    #so if we reverse the lookup and go from locations back to seed, we have to do at max 79 million 
    #calculations and the first location that reaches a slice of seeds is the minimum location.
    #This guarantees to find a reasonably fast solution, and is easier as
    #keeping track of intervals and splits of intervals, if we would go from seed interval to location.
    maxloc = 79753136
    maplist.reverse()
    mlist = maplist
    stop = False
    for i in range(0,maxloc):
      if i %1000000 == 0 :
          print('we are at location: ' + str(i) )
      index = i
      for mapl in mlist:
          index = mapl.get_index(index)

      for snum in range(0,len(seedlist),2):
          if seedlist[snum] <= index and (seedlist[snum] + seedlist[snum+1] - 1) >= index:
              print('seed: ' + str(index))
              print('between: ' + str(seedlist[snum]))
              minloc = i 
              stop = True
              break
      if stop:
          break


    print('minloc: ', minloc)


if __name__ == "__main__":
    main()

