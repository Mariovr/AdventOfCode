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
sys.setrecursionlimit(99999999)
from collections import Counter, defaultdict, deque #defaultdict provides default function when accessing key not present
from copy import deepcopy
import re

with open('input21.txt','r') as aoc:
    text = aoc.read()
inpa = text.strip().split('\n')
stringlist ="""029A
980A
179A
456A
379A
"""
#inpa = [line.strip() for line in stringlist.strip().split('\n')]
print(inpa)

class KeyPad(object):
    def __init__(self, target = '' , pos = (3,2), cache = {}):
        self.pos = pos
        self.apos = pos
        self.target = target
        self.movedir = {'>':[0, 1], 'v':[1, 0] , '<':[0, -1] ,'^' :[-1, 0] , 'A': 'A' }
        self.pressed_buttons = []
        self.moves = []
        self.num_p_but = len(self.pressed_buttons)
        self.pad = []
        self.cache = cache

    def move(self, d):
        assert d in self.movedir
        self.moves.append(d)
        if d != 'A':
            self.pos = (self.pos[0] + self.movedir[d][0], self.pos[1] + self.movedir[d][1])
            assert self.pad[self.pos[0]][self.pos[1]] != ''
        else:
            self.pressed_buttons.append(self.pad[self.pos[0]][self.pos[1]])
            self.num_p_but +=1
            assert ''.join(self.pressed_buttons)[:self.num_p_but] == self.target[:self.num_p_but]

    def get_move_string(self):
        return ''.join(self.moves)

    def set_dims(self):
        self.dimx = len(self.pad)
        self.dimy = len(self.pad[0])
        #print('dimx: ' , self.dimx , ' dimy: ' , self.dimy)

    def find_target(self,targ):
        if targ in self.cache:
            for t in self.cache[targ]:
                self.move(t)
        moves = []
        for i , t in enumerate(targ):
            #print('search' , t)
            #print('sstart' , self.pos)
            #print('target' , self.target)
            #print(self.pad)
            #print(self.pos)
            if t == self.pad[self.pos[0]][self.pos[1]]:
                moves += ['A']
                #print('same: ' , self.pos , moves)
                continue
            d = deque([([], self.pos[0] , self.pos[1])])
            seen = set()
            while(d):
                op, xc , yc = d.popleft()
                seen.add((xc,yc))
                for mv in ['^','<','>','v']:
                    nx = xc + self.movedir[mv][0]
                    ny = yc + self.movedir[mv][1]
                    if 0 <= nx < self.dimx and 0<= ny < self.dimy and (nx,ny) not in seen:
                        if self.pad[nx][ny] == '':
                            continue
                        elif self.pad[nx][ny] == t:
                            #to make sure that similar operations follow each other for a shortest sequence, and to avoid going through a blank spot on the pad.
                            moves += self.short_sort(op + [mv],self.pos, t) + ['A']
                            self.pos = (nx,ny)
                            d = False
                            break
                        else:
                            np = op + [mv]
                            d.append((np, nx ,ny))
                    else:
                        continue

        #check moves where oke
        #print(moves)
        self.pos = self.apos
        for m in moves:
            self.move(m)
        self.cache[targ] = ''.join(self.moves)

    def __str__(self):
        outputstr = 'Position: ' + str(self.pos)+ ' press history: '  + str(self.pressed_buttons) + '\n'
        outputstr += 'Nmoves: ' + str(len(self.moves))+ ' move history: '  + str(self.moves) + '\n'
        return outputstr

class NKeyPad(KeyPad):
    def __init__(self, target , pos = (3,2), cache = {}):
        super(NKeyPad,self).__init__(target,pos, cache)
        self.pad = [['7','8','9'],['4','5','6'],['1','2','3'],['','0','A']]
        self.set_dims()

    def short_sort( self , sl, opos, t):
        #to avoid going through a '', but need to make sure that if possible the keys are pressed in the order < v and only then one of < or >, as it will minimise the length of dir. keypad presses.
        if opos[0] == self.dimx-1:
            if t in ['1','4','7']:
                return sorted(sl , key = lambda x : 0 if x == '^'  else ( 1 if x== '<' else ( 2 if x == '>' else 3 ) ) )
            else:
                return sorted(sl , key = lambda x : 0 if x == '<'  else ( 1 if x== 'v' else ( 2 if x == '>' else 3 ) ) )
        elif opos[1] == 0 and t in ['0' , 'A']:
            return sorted(sl , key = lambda x : 0 if x == '>'  else ( 1 if x== 'v' else ( 2 if x == '^' else 3 ) ) )
        else:
            return sorted(sl , key = lambda x : 0 if x == '<'  else ( 1 if x== '^' else ( 2 if x == 'v' else 3 ) ) )

class DKeyPad(KeyPad):
    def __init__(self, target , pos = (0,2), cache = {}):
        super(DKeyPad,self).__init__(target,pos, cache)
        self.pad = [['','^','A'],['<','v','>']]
        self.set_dims()

    def short_sort( self , sl, opos, t):
        return sorted(sl , key = lambda x : 0 if x == 'v'  else ( -1 if x== '>' else 2 ) )

def part1():
    res = 0
    numb = 2
    for i, line in enumerate(inpa):
        print('####num line: ' , i , line)
        nkp = NKeyPad(line)
        nkp.find_target(line)
        target = nkp.get_move_string()
        cache = {}
        for j in range(numb):
            #print('num bot: ' , j)
            dkp1 = DKeyPad(target, cache = cache)
            dkp1.find_target(target)
            target = dkp1.get_move_string()
            cache = dkp1.cache
        num = int(line[:-1]) * len(dkp1.moves)
        print('moves:' , dkp1.moves, 'comp: ' , num, 'length: ' ,len(dkp1.moves))
        res += num
    return res

def part2():
    pass

result1 = part1()
#result2 = part2()
# Submit
print('Result 1:', result1)
#aoc.submit(2, result1)
#print('Result 2:', result2)
#aoc.submit(2, result2)

