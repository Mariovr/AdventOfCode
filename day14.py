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
import copy

class Rmap(object):

    def __init__(self, rmap):

        self.rmap = rmap
        self.vdim = len(rmap)
        self.results = []
        self.cyclestarted = False
        self.cycleended = False
        self.cycle = []
        self.startposcycle = 0
        self.saves = ['']*5
        self.ccmap = []

    def solve_a(self):
        self.ccmap = self.rotate_cnt_clockwise(self.rmap)
        self.move_left()
        self.ccmap = self.rotate_clockwise(self.ccmap)
        self.make_string()
        return self.count_points(self.ccmap)

    def run_cycle(self):
        self.ccmap = self.rotate_cnt_clockwise(self.rmap)
        numc = 0
        while not self.cycleended:
            self.move_left()
            self.ccmap = self.rotate_clockwise(self.ccmap)
            self.move_left()
            self.ccmap = self.rotate_clockwise(self.ccmap)
            self.move_left()
            self.ccmap = self.rotate_clockwise(self.ccmap)
            self.move_left()
            self.ccmap = self.rotate_clockwise(self.ccmap)
            self.ccmap = self.rotate_clockwise(self.ccmap)
            self.make_string()
            result = self.count_points(self.ccmap)
            if self.cyclestarted and result == self.cycle[0]:
                if self.savestartmap == self.ccmap:
                    self.cycleended = True
            if self.cyclestarted and not self.cycleended:
                self.cycle.append(result)
            if  not self.cyclestarted and self.check_cycle(result, numc):
                self.cyclestarted = True
                self.safe_cycle = self.ccmap
                self.cycle.append(self.results[-4])
                self.cycle.append(self.results[-3])
                self.cycle.append(self.results[-2])
                self.cycle.append(self.results[-1])
                self.cycle.append(result)
            self.results.append(result)
            self.saves[numc%5] = self.ccmap
            numc += 1
            self.ccmap = self.rotate_cnt_clockwise(self.ccmap)
            self.startpos = len(self.cycle) - self.startposcycle
        #print(self.ccmap)

    def check_cycle(self, num,numc):
        for i in range(len(self.results)-5,1,-1):
            if self.results[i] == num and self.results[i-1] == self.results[-1] and self.results[i-2] == self.results[-2] and self.results[i-3] == self.results[-3] and self.results[i-4] == self.results[-4]:
                self.startposcycle = i-4
                self.savestartmap = self.saves[(numc-4)%5]
                return True
        return False

    def rotate_cnt_clockwise(self, inputlist):
        ccmap = []
        for i in range(len(inputlist[0])-1,-1 , -1):
            ccmap.append([listitem[i] for listitem in inputlist])
        return ccmap

    def rotate_clockwise(self, inputlist):
        ccmap = []
        for i in range(0,len(inputlist[0]) ):
            d = [listitem[i] for listitem in inputlist]
            d.reverse()
            ccmap.append(d)
        return ccmap

    def move_left(self):
        for i in range(len(self.ccmap)):
            path = ''.join(self.ccmap[i])
            pattern = re.finditer(r'#',path)
            sindex = 0
            for pat in pattern:
                rocks = re.findall(r'O' , path[sindex:pat.start()] )
                numO = len(rocks)
                for j in range(sindex,sindex+ numO):
                    self.ccmap[i][j] = 'O' 
                for j in range(sindex+numO, pat.start()):
                    self.ccmap[i][j] = '.'
                sindex = pat.start()+1
            rocks = re.findall(r'O' , path[sindex:] )
            numO = len(rocks)
            for j in range(sindex,sindex+ numO):
                self.ccmap[i][j] = 'O' 
            for j in range(sindex+numO, len(self.ccmap[i])):
                self.ccmap[i][j] = '.'

    def count_points(self, inputlist):
        cnt = 0
        for i in range(len(inputlist)):
            reslist = re.findall(r'O' , inputlist[i])
            cnt += len(reslist) * (len(inputlist) - i)
        return cnt

    def make_string(self):
        for i in range(len(self.ccmap)):
            self.ccmap[i] = ''.join(self.ccmap[i])

    def make_list(self):
        for i in range(len(self.ccmap)):
            self.ccmap[i] = self.ccmap[i].split()


    def __str__(self):
        outputstr += 'Rmap: \n' 
        for line in self.rmap:
            #lines += ''.join(line) + '\n'
            outputstr += str(line) + '\n'
        outputstr +='\n'
        outputstr += 'CCmap: \n' 
        for line in self.ccmap:
            #lines += ''.join(line) + '\n'
            outputstr += str(line) + '\n'
        outputstr +='\n'
        return outputstr


def main(*args , **kwargs):

    maplist = []
    for line in lines:
        #print(line)
        maplist.append(line)

    rmap = Rmap(maplist)
    print('Result a: ' , rmap.solve_a())

    #For question b: observing learns that there is a cycle of length 9, that starts at position 176.
    #so the result can be found as: (1000000000-176)%9 = 5 extra full rot. of the cycle
    #The cycle starts at 99621 and after 5th additional full rotations: answer is 99641.
    rmap.run_cycle()
    reslist = rmap.results
    d = list(zip(range(len(reslist)) , reslist))
    print(d)

    rindex =  (1000000000 - rmap.startposcycle-1) % len(rmap.cycle)
    result = rmap.cycle[rindex]
    print(rmap.startposcycle)
    print(rmap.cycle)
    print(rindex)
    print(result)

    return result

if __name__ == "__main__":
    stringlist ="""O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""
    lines = [line.strip() for line in stringlist.strip().split('\n')]
    assert main(lines) == 64

    file = "inputday14.txt"
    with open(file,'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    result = main(lines)
    print('Result is: ', result)



