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

def main(*args , **kwargs):
    file = "inputday3.txt"
    objectlist = []
    skip = '.'
    totsum = 0

    with open(file,'r') as f:
        data = f.readlines()
        for index,line in enumerate(data):
            print(line)
            pattern = re.finditer(r'(\d+)',line)
            for pat in pattern:
                includesum = False
                if pat.start() > 0:
                    startp = pat.span()[0]-1
                else:
                    startp = 0
                if pat.end() < 140:
                    endp = pat.span()[1]+1
                else:
                    endp = pat.span()[1]

                if index >0 :
                    print(data[index-1][startp:pat.end()+1 ] )
                    match = re.search(r'[^.0-9]',data[index-1][startp:endp ] )
                    if match is not None:
                       includesum = True

                print (data[index][startp:pat.end()+1] )
                match = re.search(r'[^.0-9]',data[index][startp:endp ] )
                if match is not None:
                   includesum = True

                if index < len(data)-1:
                    print(data[index+1][startp:pat.end()+1 ] )
                    match = re.search(r'[^.0-9]',data[index+1][startp:endp ] )
                    if match is not None:
                       includesum = True

                print(includesum)
                if includesum:
                    #print(int(pat.group())
                    totsum += int(pat.group())
            #if index > 11:
                #sys.exit(1)



    print('totsum is: ' , totsum)


if __name__ == "__main__":
    main()


