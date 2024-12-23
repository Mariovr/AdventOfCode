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
from collections import Counter, defaultdict, deque #defaultdict provides default function when accessing key not present
from functools import reduce

with open('input21.txt','r') as f:
    text = f.read()
inpa = text.strip().split('\n')
stringlist ="""029A
980A
179A
456A
379A
"""
#inpa = [line.strip() for line in stringlist.strip().split('\n')]

class KeyPad(object):
    def __init__(self, target = '' , pos = (3,2), cache = {}):
        self.pos = pos
        self.apos = pos
        self.target = target
        self.movedir = {'>':[0, 1], 'v':[1, 0] , '<':[0, -1] ,'^' :[-1, 0] , 'A': 'A' }
        self.pressed_buttons = []
        self.moves = ''
        self.num_p_but = 0
        self.pad = []
        self.cache = cache

    def move(self, d): #test function used by check_moves.
        assert d in self.movedir
        self.moves += d
        if d != 'A':
            self.pos = (self.pos[0] + self.movedir[d][0], self.pos[1] + self.movedir[d][1])
            assert self.pad[self.pos[0]][self.pos[1]] != ''
        else:
            self.pressed_buttons.append(self.pad[self.pos[0]][self.pos[1]])
            self.num_p_but += 1
            assert ''.join(self.pressed_buttons)[:self.num_p_but] == self.target[:self.num_p_but]
        assert self.num_p_but == self.moves.count('A')

    def check_moves(self, movel):
        #test function to check if everything is fine
        self.pos = self.apos #make sure we start from the A on the keypad.
        self.moves = ''
        self.num_p_but = 0
        for m in movel:
            self.move(m)
        #print(self.pressed_buttons)

    def get_move_string(self, target):
        self.target = target
        if self.moves == '':
            self.moves, self.pos = self.find_target(self.target, self.pos)
            return self.moves
        else:
            nm, self.pos  = self.find_target(self.target, self.pos)
            self.moves += nm
            return self.moves

    def set_dims(self):
        self.dimx = len(self.pad)
        self.dimy = len(self.pad[0])

    def find_target(self,targ, startpos):
        if (targ,startpos) in self.cache:
            return self.cache[(targ,startpos)]
        moves = ''
        endpos = (startpos[0] , startpos[1])
        for i , t in enumerate(targ):
            if t == self.pad[endpos[0]][endpos[1]]:
                moves += 'A'
                continue
            d = deque([('',endpos[0] ,endpos[1])])
            seen = set()
            while(d):
                op, xc , yc = d.popleft()
                seen.add((xc,yc))
                for mv in ['<','^','>','v']:
                    nx = xc + self.movedir[mv][0]
                    ny = yc + self.movedir[mv][1]
                    if 0 <= nx < self.dimx and 0<= ny < self.dimy and (nx,ny) not in seen:
                        if self.pad[nx][ny] == '':
                            continue
                        elif self.pad[nx][ny] == t:
                            #to make sure that similar operations follow each other for a shortest sequence, and to avoid going through a blank spot on the pad.
                            moves += ''.join(self.short_sort(op + mv,endpos, t)) + 'A'
                            endpos = (nx,ny)
                            d = False
                            break
                        else:
                            np = op + mv
                            d.append((np, nx ,ny))
                    else:
                        continue
        self.cache[(targ,startpos)] = (moves, endpos)
        return moves, endpos

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
        #to avoid going through a '', but need to make sure that if possible the keys are pressed in the order < v and only then one of ^ or >, as it will minimise the length of dir. keypad presses.
        if opos[0] == self.dimx-1:
            if t in ['1','4','7']:
                return sorted(sl , key = lambda x : 0 if x == '^'  else ( 1 if x== '<' else ( 2 if x == '>' else 3 ) ) )
            else:
                return sorted(sl , key = lambda x : 0 if x == '<'  else ( 1 if x== '^' else ( 2 if x == 'v' else 3 ) ) )
        elif opos[1] == 0 and t in ['0' , 'A']:
            return sorted(sl , key = lambda x : 0 if x == '<'  else ( 1 if x== '>' else ( 2 if x == 'v' else 3 ) ) )
        else:
            return sorted(sl , key = lambda x : 0 if x == '<'  else ( 1 if x== 'v' else ( 2 if x == '^' else 3 ) ) )

class DKeyPad(KeyPad):
    def __init__(self, target , pos = (0,2), cache = {}):
        super(DKeyPad,self).__init__(target,pos, cache)
        self.pad = [['','^','A'],['<','v','>']]
        self.set_dims()

    def short_sort( self , sl, opos, t):
        #sort sequence duplicates should always follow each other.
        #if possible (paths through a blank are not possible) < should come before v before ^ , some cases are not possible then go for 2nd best ordering.
        if opos[0] == 1 and opos[1] == 0 and t == 'A':
            return '>>^'
        elif opos[0] == 0 and opos[1] == 2 and t == '<':
            return 'v<<'
        elif opos[0] == 1 and opos[1] == 0:
            return sorted(sl , key = lambda x : 0 if x == '>'  else ( 1 if x== '^' else 2 ) )
        elif opos[0] == 1 and opos[1] == 2:
            return sorted(sl , key = lambda x : 0 if x == '<'  else ( 1 if x== '^' else 2 ) )
        elif opos[0] == 0 and opos[1] == 1:
            return sorted(sl , key = lambda x : 0 if x == 'v'  else ( 1 if x== '<' else 2 ) )
        else:
            return sorted(sl , key = lambda x : 0 if x == '^'  else ( 1 if x== '>' else 2 ) )

def get_a_parts(target, cnt = 1):
    #parts of the string that ends at A, and starts at A we can treat independently so for all copies we only have to do the calculations once.
    #Checking the cache we see that sometimes for a full string after 12 iterations still it is completely covered by only a few A -> A character strings, so there is a huge amount of repetition.
    Aind = [ i for i, c in enumerate(target) if c == 'A']
    dif = list(zip([-1] + Aind , Aind + [len(target) ] ))
    partcount = Counter()
    for i , j in dif:
        text = target[i+1:j+1]
        if text != '':
            partcount[text] +=1 *cnt
    return partcount

def iterate(target, n):
    cache = {}
    pc = get_a_parts(target)
    resl = []
    for j in range(n):
        dkp1 = DKeyPad(pc.most_common(), cache = cache)
        countl = []
        for part, cnt in pc.items():
            target, endpos = dkp1.find_target(part, (0, 2)) #all parts start at start position, and end there as well.
            npc = get_a_parts(target, pc[part])
            countl.append(npc)
            assert endpos == (0,2)
        pc = reduce(lambda x,y : x+y, countl) #get sum of all counters in one counter
        cache = dkp1.cache
        #print('cache size: ' , len(cache))
        if j == 1 or j == n-1:
            res = 0
            for part, cnt in pc.items():
                res += len(part) * cnt
            resl.append(res)
    return resl[0] , resl[1]

def parts():
    res1, res2 = 0,0
    nump = 25
    #nump = 10000 #code is so fast that it also works for 10000 subsequent keypads in a few seconds :).
    for i, line in enumerate(inpa):
        print('####num line: ' , i , line)
        nkp = NKeyPad(line)
        target = nkp.get_move_string(line)
        len1, len2 = iterate(target,nump)
        res1 += int(line[:-1]) * len1
        res2 += int(line[:-1]) * len2
    return res1,res2

result1, result2 = parts()
print('Result 1:', result1)
print('Result 2:', result2)

