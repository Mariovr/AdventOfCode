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

import os
import sys
import re
from itertools import product

class Equation(object):
    def __init__(self, result , numbers):
        self.result = result
        self.numbers = numbers
        self.valid = False
        self.operators = ['*'] * (len(self.numbers) - 1)

    def check_valid(self):
        ops = ['*' ,'+'] 
        comb = product( ops, repeat = len(self.operators) )
        for opl in list(comb):
            res = self.numbers[0]
            for i,op in enumerate(opl):
                if op == '*':
                    res *= self.numbers[i+1] 
                else:
                    res += self.numbers[i+1]
            if res == self.result:
                self.valid = True
                self.operators =list(opl)
                break

    def check_valid2(self):
        ops = ['*' ,'+', '|'] 
        comb = product( ops, repeat = len(self.operators) )
        for opl in list(comb):
            res = self.numbers[0]
            for i,op in enumerate(opl):
                if op == '*':
                    res *= self.numbers[i+1] 
                elif op == '+':
                    res += self.numbers[i+1]
                else:
                    res = int(str(res) + str(self.numbers[i+1]))

            if res == self.result:
                self.valid = True
                self.operators =list(opl)
                break

    def __str__(self):
        outputstr = 'Result =  ' + str(self.result) + ' = '
        for i , num in enumerate(self.numbers):
            outputstr += str(num) + ' '   
            if i < len(self.numbers)-1:
                outputstr += str(self.operators[i])
        outputstr += '\n'
        return outputstr

def main(args , **kwargs):
    result = 0
    eqlist = []
    for i, line in enumerate(args):
        match = re.search('(\d+):\s([\s\d]+)', line)
        eqlist.append(Equation(int(match.group(1)) , [int(num) for num in match.group(2).split()]))
        eqlist[i].check_valid2()
        if eqlist[i].valid:
            result += eqlist[i].result

    return result

if __name__ == "__main__":
    stringlist ="""190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""

    lines = [line.strip() for line in stringlist.strip().split('\n')]
    assert main(lines) == 11387

    file = "input7.txt"
    with open(file,'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    result = main(lines)
    print('Result is: ', result)



