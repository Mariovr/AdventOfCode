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
from itertools import combinations

class Park(object):

    def __init__(self, groups, field):

        self.groups= groups
        self.field = field
        self.numb = sum(self.groups)
        self.nump = len(self.field)
        self.numg = self.nump-self.numb
        self.qs = [ index for index, q in enumerate(self.field) if q == '?' ]
        self.countge = self.field.count('.')

    def distribute(self):
        combs= combinations(self.qs ,self.numg-self.countge)
        for poslist in list(combs):
            teststring = self.field
            for p in poslist:
                teststring = teststring[:p] + '.' + teststring[p+1:]
            yield teststring

    def count_goods(self):
        result = 0
        for text in list(self.distribute()):
            if self.test(text):
                result += 1
        return result

    def test(self, string):
        res = re.findall(r'[#?]+',string) #we put the good ones so all # and ? still left are broken.
        for index, i in enumerate(res):
            if len(i) == self.groups[index]:
                pass
            else:
                return False
        return True


    def __str__(self):
        outputstr = 'num broken: ' + str(self.numb) + '\n'
        outputstr += 'num positions: ' + str(self.nump) + '\n'
        outputstr += 'num good: ' + str(self.numg) + '\n'
        outputstr += 'groups: ' + str(self.groups) + '\n'
        outputstr += 'field: ' + str(self.field) + '\n'
        outputstr += 'num good already there: ' + str(self.countge) + '\n'
        return outputstr


def main(*args , **kwargs):

    result = 0
    for line in lines:
        d = line.split(' ')
        field = Park([int(num) for num in d[1].split(',')], d[0])
        result += field.count_goods()

    return result

if __name__ == "__main__":
    stringlist ="""???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""
    lines = stringlist.strip().split('\n')
    print (lines)
    assert main(lines) == 21

    file = "inputday12.txt"
    with open(file,'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    result = main(lines)
    print('Result is: ', result)












