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
import sys
from aoc import AOC

if len(sys.argv) > 1:
    example = open(sys.argv[1]).read().strip()
    inpa = [line.strip() for line in example.strip().split('\n')]
else:
    aoc = AOC(11 , 2015)
    inpa = aoc.input.strip().split('\n')

lstring = 'abcdefghijklmnopqrstuvwxyz'
print(inpa)

def valid(s):
    for inv_c in ['i','l','o' ]: #check if any invalid char in s
        if inv_c in s:
            return False
    if len( [i for i in range(0,len(s) - 2, 1) if s[i:i+3] in lstring] ) == 0: #check if 3l alph. increas seq in s.
        return False
    i,npair = 0,0
    while i < len(s)-1 :
        if s[i] == s[i+1]:
            npair += 1
            i+=1 #to avoid overlapping pairs
        i +=1
    return npair >= 2

def step_password(line, ind):
    for i , indext in enumerate(ind[::-1]):
        line_i , char_i = indext
        if char_i != 25: #find first index that is not resetting back to a, then augment it with one and break the for loop for the next iteration.
            line[line_i] = lstring[char_i+1]
            ind[len(ind) - 1 - i ] = (line_i , char_i+1)
            break
        else: #wrap this char back to a
            line[line_i] = 'a'
            ind[len(ind) - 1-i ] = (line_i , 0) #index of a in lstring
    return line

def parts():
    line = list(inpa[0])
    ind = [(i, lstring.index(c) ) for i, c in enumerate(line) ] #get all the indexes of constituents of the string in lstring
    for n in range(2): #answers are the subsequent valid passwords.
        while(not valid(''.join(line))):
            line = step_password(line, ind)
        if n == 0:
            res1 = ''.join(line)
            step_password(line,ind)
        else:
            res2 = ''.join(line)
    return res1, res2


res1, res2 = parts()
print('Result 1:', res1)
print('Result 2:', res2)
