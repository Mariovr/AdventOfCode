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
import numpy as np
import re

class Park(object):

    def __init__(self, groups, field, mult = 1):

        self.g= groups
        self.f = field
        self.mult = mult
        self.cache = {}
        self.set_mult_data()
        print(self.locations)

    def set_mult_data(self):
        self.groups = self.g*self.mult
        self.field = '?'.join([ self.f for i in range(self.mult)])
        self.locations = [ [i, 0]      for i in self.groups]   
        for index in range(len(self.locations)):
            self.locations[index][1] = sum(self.groups[:index])+ 1 * index #to add 1 for extra . at end of # list
        self.ngroups = len(self.groups)
        self.tpos = len(self.field)
        self.cacheindex = (self.ngroups / 5, self.ngroups*2/5 , self.ngroups*3/5, self.ngroups*4/5)

    def cnt_placements(self, sindex):
        cnt = 0
        ckey = ','.join([ str(loc[1]) for loc in self.locations[sindex:]] )
        if ckey in self.cache.keys():
            return self.cache[ckey]
        plist = self.get_placements(sindex)
        #print('plist: ' , plist)
        for p in plist:
            self.locations[sindex][1]= p
            if sindex+1 < self.ngroups: #update starts of the next
                for uindex in range(sindex, self.ngroups-1):
                    self.locations[uindex+1][1] = self.locations[uindex][0]+ self.locations[uindex][1]+ 1  #to add 1 for extra . at end of # list
            #print('locations after reset: ' , self.locations)
            if self.locations[-1][0] + self.locations[-1][1] > self.tpos:
                break
            if sindex +1< self.ngroups:
                #print('cnt: ', cnt)
                cnt += self.cnt_placements(sindex+1)
            else:
                if self.valid_end(p):
                    cnt += 1
        if sindex in self.cacheindex:
            self.cache[ckey] = cnt
        return cnt

    def get_placements(self, index):
        #print('index: ' ,index)
        placelist = []
        cont = True
        last = False
        startpos = self.locations[index][1]
        if index == self.ngroups -1:
            last = True
        while ( cont):
            test = self.place(self.field, self.locations[index][0], startpos, last)
            if test == -1:
                cont = False
                #print('cont: ' , cont)
            else:
                startpos = test + 1
                if self.valid_place(index, test):
                    placelist.append(test)
        return placelist

    def valid_place(self,index,test):
        if index == 0:
            start = 0
        else:
            start = self.locations[index-1][0] + self.locations[index-1][1]
        if '#' in self.field[start:test]:
            #print('invalid place')
            return False
        else:
            return True

    def valid_end(self, test):
        if '#' in self.field[test+ self.locations[-1][0]:]:
            #print('invalid end')
            return False
        else:
            #print('valid end: ' )
            return True

    def place(self, line, length , startpos, last = False):
        if last:
            regexp = r'[#?]{' + re.escape(str(length)) + '}'
            res = re.search(regexp,line[startpos:])
        else:
            regexp = r'[#?]{' + re.escape(str(length))+ '}[.?]' 
            res = re.search(regexp,line[startpos:])
        if  res is None:
            #print('not match')
            return -1
        else:
            #print('match: ', res.start() + startpos)
            return res.start() + startpos

    def __str__(self):
        outputstr += 'groups: ' + str(self.groups) + '\n'
        outputstr += 'field: ' + str(self.field) + '\n'
        return outputstr


def main(*args , **kwargs):

    result = 0
    for line in lines:
        d = line.split(' ')
        field = Park([int(num) for num in d[1].split(',')], d[0], mult = 5)
        iresult = field.cnt_placements(0)

        print('iresult: ',iresult )
        result += iresult

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
    print(lines)
    result = main(stringlist)
    print('Result is: ', result)
    assert result == 525152

    file = "inputday12.txt"
    with open(file,'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    result = main(lines)
    print('Result is: ', result)












