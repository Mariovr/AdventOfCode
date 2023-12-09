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
from math import lcm
import numpy as np

class Node(object):

    def __init__(self, node, ldir , rdir):

        self.node = node
        self.ldir = ldir
        self.rdir = rdir

    def step(self,d):
        if d == 'L':
            return self.ldir
        else:
            return self.rdir

    def __str__(self):
        outputstr = 'node: ' + str(self.node) + '\n'
        outputstr += 'rdir: ' + str(self.rdir) + '\n'
        outputstr += 'ldir: ' + str(self.ldir) + '\n'
        return outputstr

def main(*args , **kwargs):
    file = "inputday8.txt"
    steps = []
    dirlist = {}

    with open(file,'r') as f:
        lines = f.readlines()
        steps = [c for c in lines[0].strip() ]
        print(steps)
        for line in lines[1:]:
            tup = re.findall(r'\w{3}',line)
            if len(tup ) >1:
                dirlist[tup[0]] = Node(tup[0],tup[1],tup[2])

    startnodes = [ snode for snode in dirlist.values() if snode.node[2] == 'A'] 
    pathlen = list([''] * len(startnodes))

    for index , startnode in enumerate(startnodes):
        stepi = 0
        numstep = 0
        while(startnode.node[2] != 'Z' ):
            newnodekey = startnode.step(steps[stepi])
            startnode = dirlist[newnodekey] 
            stepi += 1
            stepi = stepi % len(steps)
            numstep += 1

        print(str(dirlist[startnode.step(steps[stepi])] ) )

        pathlen[index] = numstep
        print('numstep: ' , numstep)
        print('stepi: ' ,stepi)
        print('node: ' , startnode)

    #lcm idea just works because the length to get from A node to Z is equal to the period of the cycle, no way to assume this from description only by observing the Z -> Z cycle after each start.
    #Got the idea from the internet.
    #However it made the problem trivial and could not undo it from my brain.

    print('result: ', lcm(*pathlen))


if __name__ == "__main__":
    main()
