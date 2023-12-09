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


class Pyramid(object):

    def __init__(self, vallist):

        self.pyr = [vallist]
        self.construct_pyramid()
        self.create_history()

    def construct_pyramid(self):
        while(sum(self.pyr[-1]) != 0):
            self.pyr.append(list( self.construct_slice(self.pyr[-1])) )

    def construct_slice(self, vl):
        for index, num in enumerate(vl[:-1]):
            yield  vl[index+1] - num

    def create_history(self):
       self.pyr[-1] = [0] + self.pyr[-1] 
       for num in range(len(self.pyr)-1, 0,-1) :
           snum =  self.pyr[num-1][0] - self.pyr[num][0] 
           self.pyr[num-1] = [snum] + self.pyr[num-1]

    def __str__(self):
        outputstr = 'Values: ' + str(self.pyr) + '\n'
        return outputstr


def main(*args , **kwargs):
    file = "inputday9.txt"
    objectlist = []

    with open(file,'r') as f:
        for line in f:
            vallist = [ int(num) for num in line.strip().split(' ')]
            pyr = Pyramid(vallist)
            objectlist.append(pyr)
            print(pyr)

    totnum = 0 
    for pyr in objectlist:
        totnum += pyr.pyr[0][0]
    print('totnum: ' , totnum)

if __name__ == "__main__":
    main()
