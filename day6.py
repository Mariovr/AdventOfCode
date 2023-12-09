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


class Race(object):

    def __init__(self,value):

        self.value = 0

    def __str__(self):
        outputstr = 'value: ' + str(self.value) + '\n'
        outputstr += ''
        return outputstr

def win(time,distance, i):
    if i * (time-i) > distance:
       return True
    else:
       return False

def main(*args , **kwargs):
    file = "inputday6.txt"
    objectlist = []

    
    with open(file,'r') as f:
        lines = f.readlines()
    times = re.findall(r'\d+', lines[0])
    times = ''.join(times)
    times = int(times)
    print(times)
    dist = re.findall(r'\d+', lines[1])
    dist= ''.join(dist)
    dist = int(dist)
    print(dist)

    d = list(range(0,55000000))
    saveh1 =0 
    for i in d:
        #print(i)
        if  win(times,dist,i):
            print('ht: ' + str(i) + ' time: ' + str(times) )
            saveh1 = i
            break
    d.reverse()

    for i in d:
        #print(i)
        if  win(times,dist,i):
            print('ht: ' + str(i) + ' time: ' + str(times) )
            break
    d.reverse()

    print('result: ' , i - saveh1 +1)


if __name__ == "__main__":
    main()
