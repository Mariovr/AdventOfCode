# This program is free software. It comes without any warranty, to the extent
# permitted by applicable law. You may use it, redistribute it and/or modify
# it, in whole or in part, provided that you do so at your own risk and do not
# hold the developers or copyright holders liable for any claim, damages, or
# other liabilities arising in connection with the software.
# 
#Developed by Mario Van Raemdonck, 2024;
#
# -*- coding: utf-8 -*-
#! /usr/bin/env python 

import re

def main():
    result = 0
    file = "input3.txt"

    with open(file,'r') as f:
        lines = f.read()
        lines.join('\n')

    pattern = re.search(r'don\'t\(\)', lines)
    while(pattern is not None):
        eindex = lines[pattern.span()[0]:].find('do()')
        if eindex > 0:
            lines = lines[:pattern.span()[0]] + lines[pattern.span()[0]+eindex+4:]
        else:
            lines = lines[:pattern.span()[0]]
        pattern = re.search(r'don\'t\(\)', lines)

    reg = re.findall(r'mul\((\d+),(\d+)\)',lines)
    for i , j  in reg:
        result += int(i) * int(j)
    print('result: ' , result)

if __name__ == "__main__":
    main()


