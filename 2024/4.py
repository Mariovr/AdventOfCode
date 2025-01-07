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

def main1(args , **kwargs):
    result = 0
    for j, line in enumerate(args):
        indexes = [i for i, ltr in enumerate(line) if ltr == 'X']
        for a in indexes:
            if line[a:a+4] == 'XMAS':
                result += 1
            if line[a-3:a+1][::-1] == 'XMAS':
                result += 1
            if j +3 < len(args):
                if ''.join([args[j + b][a] for b in range(4)  ]) == 'XMAS':
                    result += 1
            if j - 3 >=  0:
                if ''.join([args[j - b][a] for b in range(4)  ]) == 'XMAS':
                    result += 1
            if a + 3 <  len(line) and j +3 < len(args):
                if ''.join([args[j + b][a+b] for b in range(4)  ]) == 'XMAS':
                    result += 1
            if a + 3 <  len(line) and j - 3 >= 0:
                if ''.join([args[j - b][a+b] for b in range(4)  ]) == 'XMAS':
                    result += 1
            if a - 3 >=  0 and j + 3 < len(args):
                if ''.join([args[j + b][a-b] for b in range(4)  ]) == 'XMAS':
                    result += 1
            if a - 3 >=  0 and j - 3 >= 0:
                if ''.join([args[j - b][a-b] for b in range(4)  ]) == 'XMAS':
                    result += 1

    return result

def main(args , **kwargs):
    result = 0
    for j, line in enumerate(args):
        indexes = [i for i, ltr in enumerate(line) if ltr == 'A']
        for a in indexes:
            if a + 1 <  len(line) and j +1 < len(args) and a - 1 >= 0 and j-1 >= 0:
                if (args[j+1][a+1] == 'S' and args[j-1][a-1] == 'M') or (args[j+1][a+1] == 'M' and args[j-1][a-1] == 'S'):
                    if (args[j+1][a-1] == 'S' and args[j-1][a+1] == 'M') or (args[j+1][a-1] == 'M' and args[j-1][a+1] == 'S'):
                        result += 1



    print(result)
    return result

if __name__ == "__main__":
    stringlist ="""MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""

    lines = [line.strip() for line in stringlist.strip().split('\n')]
    print(lines)
    assert main(lines) == 9

    file = "input4.txt"
    with open(file,'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    result = main(lines)
    print('Result is: ', result)



