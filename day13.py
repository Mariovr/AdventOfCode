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

class Pattern(object):
    def __init__(self, pat, hmult = 100, vmult= 1):
        self.pat = pat
        self.hdim = len(self.pat)
        self.vdim = len(self.pat[0])
        self.hmir = -1
        self.vmir = -1
        self.nhmir = -2
        self.nvmir = -2
        self.vmult = vmult
        self.hmult = hmult
        self.set_h_mir()
        if self.hmir == -1:
            self.set_v_mir()
        print('start h : ' , self.hmir)
        print('start v : ' , self.vmir)

    def fix_smudge(self):
        print('START FIX SMUDGE:')
        for i in range(self.hdim):
            for j in range(self.vdim):
                c = list(self.pat[i]) 
                savevar = c[j]
                if savevar == '#':
                    c[j] = '.'
                else:
                    c[j] = '#'
                self.pat[i] = ''.join(c)

                tmirror = self.set_h_mir(new = True)
                if self.nhmir != -2:
                    return self.get_new_val()

                tmirror = self.set_v_mir(new = True)
                if self.nvmir != -2:
                    return self.get_new_val()
                c[j] = savevar
                self.pat[i] = ''.join(c)

    def set_h_mir(self, new = False):
        #print('check hmir')
        tmirror = False
        for index, line in enumerate(self.pat[:-1]):
            if self.pat[index] == self.pat[index+1]:
                tmirror = True
                #print('test for index: ' , index)
                for i in range(1,min(index+1, self.hdim - index-1)):
                    if self.pat[index-i] == self.pat[index+i+1]:
                        pass
                    else:
                        tmirror = False
                if tmirror:
                    if new and index != self.hmir:
                        self.nhmir = index
                        print('set nhmir: ' , self.nhmir , '  ' )
                    else:
                        self.hmir = index
        return tmirror

        
    def set_v_mir(self, new = False):
        #print('check vmir')
        tmirror = False
        for index in range(self.vdim-1):
            if [col[index] for col in self.pat] == [col[index+1] for col in self.pat]:
                tmirror = True
                for i in range(1,min(index+1, self.vdim - index-1)):
                    if [col[index-i] for col in self.pat] == [col[index+1+i] for col in self.pat]:
                        pass
                        #print('index: ' , tmirror)
                        #print([col[index-i] for col in self.pat])
                        #print([col[index+1+i] for col in self.pat])
                    else:
                        tmirror = False
                if tmirror:
                    if new and index != self.vmir:
                        self.nvmir = index
                        print('set nvmir: ' , self.nvmir , '  ' )
                    else:
                        self.vmir = index
        return tmirror
        
    def get_val(self):
        if self.vmir != -1:
            return self.vmult * (self.vmir +1)
        elif self.hmir != -1:
            return self.hmult * (self.hmir+1)
        return  0 

    def get_new_val(self):
        if self.nvmir != -2:
            return self.vmult * (self.nvmir +1)
        elif self.nhmir != -2:
            return self.hmult * (self.nhmir+1)
        return  0 

    def __str__(self):
        outputstr = 'Pat: ' + str(self.pat) + '\n'
        outputstr += 'Hmir: ' + str(self.nhmir) + '\n'
        outputstr += 'Vmir: ' + str(self.nvmir) + '\n'
        return outputstr


def main(*args , **kwargs):
    result = 0
    patlist = []
    for index, line in enumerate(lines):
        if line == '':
            pat = Pattern(patlist)
            result += pat.fix_smudge()
            #result += pat.get_val()
            #print(pat)
            print(result)
            patlist= []
        else:
            patlist.append(line)
              
    pat = Pattern(patlist)
    result += pat.fix_smudge()
    #result += pat.get_val()
    #print(pat)
    print(result)
    return result

if __name__ == "__main__":
    stringlist ="""#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""
    lines = [line.strip() for line in stringlist.strip().split('\n')]
    print( lines)
    #assert main(lines) == 405
    assert main(lines) == 400

    file = "inputday13.txt"
    with open(file,'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    result = main(lines)
    print('Result is: ', result)

