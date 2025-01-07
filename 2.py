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

def check_safe(line):
    line = [int(lin) for lin in line]
    a = line[0]
    pos = 0 
    neg = 0 
    for b in line[1:]:
        res = a-b 
        if 1 <=res <= 3:
            pos += 1
        elif -3 <= res <= -1:
            neg += 1
        a = b
    if (pos >= len(line) - 1) or (neg >= len(line) -1):
        return True
    else:
        return False

def run_w_del(line):
    for i in range(len(line)):
        line2 = line[:i] + line[i+1:]
        if check_safe(line2):
            return True
    return False


def main(args , **kwargs):
    result = 0

    for line in args:
        levels = line.split()
        if check_safe(levels):
            result += 1
        else:
            if run_w_del(levels):
                result += 1

    return result

if __name__ == "__main__":
    stringlist ="""7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""

    lines = [line.strip() for line in stringlist.strip().split('\n')]
    assert main(lines) == 4

    file = "input2.txt"
    with open(file,'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    result = main(lines)
    print('Result is: ', result)

