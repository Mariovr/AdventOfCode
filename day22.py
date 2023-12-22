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
from copy import deepcopy

class Brick(object):
    def __init__(self, startc , endc, ident):
        self.startc = startc
        sizes = [abs(s-e)+1 for s,e in zip(self.startc,endc) ] #+1 to include startp
        self.len = max(sizes)
        self.dim = sizes.index(self.len) 
        self.id = ident

    def __str__(self):
        outputstr = 'Start: ' + str(self.startc) + '\n'
        outputstr += 'Len: ' + str(self.len) + '\n'
        outputstr += 'Dim: ' + str(self.dim) + '\n'
        outputstr += 'Ident: ' + str(self.id) + '\n'
        return outputstr

class Space(object):
    def __init__(self, bricklist):
        self.bricklist = bricklist
        self.bricklist.sort(key=lambda x : x.startc[2]) #sort bricks down
        self.set_ids()
        print([str(brick) for brick in self.bricklist])
        self.space = {}
        self.occupy_space()
        print(self.space)
        self.move_bricks_down()
        print(self.space)

    def set_ids(self):
        for index, brick in enumerate(self.bricklist):
            brick.id = index

    def occupy_space(self):
        for brick in self.bricklist:
            coord = deepcopy(brick.startc)
            for i in range(brick.len):
                self.space[tuple(coord)] = brick.id
                coord[brick.dim] += 1

    def move_brick_down(self, brick):
        print(brick)
        if brick.startc[2] == 1:
            return False
        down = True
        coord = deepcopy(brick.startc)
        coord[2] -= 1
        if brick.dim != 2: #take into account vertical bricks.
            for i in range(brick.len):
                if tuple(coord) in self.space.keys():
                    down = False
                coord[brick.dim] += 1
        elif tuple(coord) in self.space.keys():
            down = False
        if down:
            brick.startc[2] -=1
            coord = deepcopy(brick.startc)
            if brick.dim != 2:
                for i in range(brick.len):
                    self.space[tuple(coord)] = brick.id
                    del self.space[(coord[0],coord[1],coord[2]+1)]
                    coord[brick.dim] += 1
            else:
                self.space[tuple(coord)] = brick.id
                del self.space[(coord[0],coord[1],coord[2]+brick.len)]
        return down

    def move_bricks_down(self):
        for brick in self.bricklist:
            print(brick)
            down = True
            while(down):
                down = self.move_brick_down(brick)
                print('moved brick down:' , brick.id)

    def count_disin_bricks(self):
        dissum = 0
        for brick in self.bricklist:
            coord = deepcopy(brick.startc)
            nosolosupport = True
            if brick.dim != 2: #take into account vertical bricks.
                coord[2] += 1
                for i in range(brick.len):
                    if tuple(coord) in self.space.keys():
                        if not self.check_other_support(coord, brick.id):
                            nosolosupport = False

                    coord[brick.dim] += 1
            else:
                coord[2] += brick.len
                if tuple(coord) in self.space.keys():
                    if not self.check_other_support(coord, brick.id):
                        nosolosupport = False

            if nosolosupport:
                print('Counted: , ', brick.id)
                dissum += 1
        return dissum


    def check_other_support(self,coord, iden):
        brick = self.bricklist[self.space[tuple(coord)]]
        startc = deepcopy(brick.startc)
        startc[2] -= 1
        if brick.dim != 2:
            for i in range(brick.len):
                if tuple(startc) in self.space.keys(): 
                    if self.space[tuple(startc)] != iden:
                        return True
                startc[brick.dim] += 1
        return False

    def __str__(self):
        for brick in self.bricklist:
            outputstr +=  str(brick)
            outputstr += '\n'
            outputstr += '\n'
        return outputstr

#(x,y,z) #bricks only extend in one horizontal dimension (either x or y never both).
def main(args , **kwargs):
    bricklist = []
    result = 0

    for index, line in enumerate(args):
        print(line)
        coord = line.split('~')
        bricklist.append(Brick([int(s) for s in coord[0].split(',')] ,[int(e) for e in coord[1].split(',')], index) )

    bl = Space(bricklist)
    result = bl.count_disin_bricks()
    print('Result is: ' , result)


    return result

if __name__ == "__main__":
    stringlist ="""1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
"""


    lines = [line.strip() for line in stringlist.strip().split('\n')]
    print(lines)
    assert main(lines) == 5

    file = "inputday22.txt"
    with open(file,'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    result = main(lines)
    print('Result is: ', result)
