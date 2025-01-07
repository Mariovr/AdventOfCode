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

def main(args , **kwargs):
    lloc = []
    rloc = []
    for line in args:
        start, end = line.split()
        lloc.append(start)
        rloc.append(end)
    lloc = sorted(lloc)
    rloc =  sorted(rloc)
    som = 0
    for a in lloc :
        sim = rloc.count(a)
        som += int(a) * sim 
    return som

if __name__ == "__main__":
    stringlist = """3   4
    4   3
    2   5
    1   3
    3   9
    3   3
"""

    lines = [line.strip() for line in stringlist.strip().split('\n')]
    print(lines)
    assert main(lines) == 31
    print('test ok!')

    file = "input1.txt"
    with open(file,'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    result = main(lines)
    print('Result is: ', result)



