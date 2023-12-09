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


class Game(object):

    def __init__(self,*args , **kwargs):

        self.status = 0

    def __str__(self):
        outputstr = 'Object' + str(self) + '\n'
        outputstr += ''
        return outputstr


def main(*args , **kwargs):
    file = "tinput3.txt"
    objectlist = []
    skip = '.'
    totprod = 0

    with open(file,'r') as f:
        data = f.readlines()
        for index,line in enumerate(data):
            print(line)
            pattern = re.finditer(r'(\*)',line)
            for pat in pattern:
                gearnum =0
                nums = [0,0]
                if pat.start() > 0:
                    startp = pat.span()[0]-3
                else:
                    startp = 0
                if pat.end() < 140:
                    endp = pat.span()[1]+3
                else:
                    endp = pat.span()[1]

                if index >0 :
                    #print(data[index-1][startp:endp ] )
                    print(data[index-1][startp:endp ] )
                    match = re.search(r'^(\d{3})',data[index-1][startp:endp ] )
                    if match is not None:
                        gearnum += 1
                        if gearnum -1< 2:
                            nums[gearnum-1] = int(match.group(1))
                    match = re.search(r'^\D(\d{2}\d*)',data[index-1][startp:endp ] )
                    if match is not None:
                        gearnum += 1
                        if gearnum -1< 2:
                            nums[gearnum-1] = int(match.group(1))
                    match = re.search(r'^\D(\d+)',data[index-1][startp+1:endp ] )
                    if match is not None:
                        gearnum += 1
                        if gearnum -1< 2:
                            nums[gearnum-1] = int(match.group(1))
                    match = re.search(r'^\D(\d+)',data[index-1][startp+2:endp ] )
                    if match is not None:
                        gearnum += 1
                        if gearnum -1< 2:
                            nums[gearnum-1] = int(match.group(1))
                    match = re.search(r'^\D(\d+)',data[index-1][startp+3:endp ] )
                    if match is not None:
                        gearnum += 1
                        if gearnum -1< 2:
                            nums[gearnum-1] = int(match.group(1))

                print (data[index][startp:endp] )
                match = re.search(r'([0-9]+)\*',data[index][startp:endp ] )
                if match is not None:
                   gearnum += 1
                   if gearnum -1< 2:
                       nums[gearnum-1] = int(match.group(1))

                match = re.search(r'\*([0-9]+)',data[index][startp:endp ] )
                if match is not None:
                   gearnum += 1
                   if gearnum -1< 2:
                       nums[gearnum-1] = int(match.group(1))

                if index < len(data)-1:
                    print(data[index+1][startp:endp ] )
                    match = re.search(r'^(\d{3})',data[index+1][startp:endp ] )
                    if match is not None:
                        gearnum += 1
                        if gearnum -1< 2:
                            nums[gearnum-1] = int(match.group(1))
                    match = re.search(r'^\D(\d{2}\d*)',data[index+1][startp:endp ] )
                    if match is not None:
                        gearnum += 1
                        if gearnum -1< 2:
                            nums[gearnum-1] = int(match.group(1))
                    match = re.search(r'^\D(\d+)',data[index+1][startp+1:endp ] )
                    if match is not None:
                        gearnum += 1
                        if gearnum -1< 2:
                            nums[gearnum-1] = int(match.group(1))
                    match = re.search(r'^\D(\d+)',data[index+1][startp+2:endp ] )
                    if match is not None:
                        gearnum += 1
                        if gearnum -1< 2:
                            nums[gearnum-1] = int(match.group(1))
                    match = re.search(r'^\D(\d+)',data[index+1][startp+3:endp ] )
                    if match is not None:
                        gearnum += 1
                        if gearnum -1< 2:
                            nums[gearnum-1] = int(match.group(1))

                    #print(data[index+1][startp:endp ] )
#                    match = re.findall(r'([0-9]+)',data[index+1][startp:endp ] )
#                    print(data[index+1][startp:endp ] )
#                    if match:
#                        #print(len(match) )
#                        nummatch = re.findall(r'([0-9]+)',data[index+1][startp:endp ] )
#                        for i in range(len(nummatch)):
#                            gearnum += 1
#                            if gearnum-1 < 2:
#                                nums[gearnum-1] = int(nummatch[i])
#
                #print(gearnum)
                #print(nums)
                if gearnum == 2:
                    #print(int(pat.group())
                    totprod += int(nums[1]) * int(nums[0])
                    print(nums)
                    print('prod: ', int(nums[1]) * int(nums[0]) )
                    print('totprod: ' , totprod)


    print('totsum is: ' , totprod)


if __name__ == "__main__":
    main()


