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
from functools import reduce
import numpy as np


class Game(object):

    def __init__(self,gamenum, drawnum , winnum):

        self.gamenum=gamenum
        self.drawnum = drawnum
        self.winnum = winnum
        self.matchnum = []
        self.score = 0
    
    def set_matchnum(self):
        self.matchnum = [   i         for i in self.winnum  if i in self.drawnum]
        print(self.matchnum)

    def get_totmatch(self):
        return len(self.matchnum)

    def set_score(self):
        if len(self.matchnum) >=  1:
            self.score = 2**(len(self.matchnum) -1 )

    def __str__(self):
        outputstr = 'Object' + str(self) + '\n'
        outputstr += ''
        return outputstr


def main(*args , **kwargs):
    file = "inputday4.txt"
    gamelist = []
    cardlist = []
    totscore = 0 

    with open(file,'r') as f:
        for line in f:
            gamenum  = re.search(r'Card\s*(\d+)\s*:',line).group(1)
            drawnum = re.findall(r'(\d+)',line[8:39])
            #print (drawnum)
            drawnum = [int(num) for num in drawnum]
            winnum = re.findall(r'(\d+)',line[40:])
            #print (winnum)
            winnum = [int(num) for num in  winnum]
            game = Game(gamenum, drawnum , winnum)
            game.set_matchnum()
            game.set_score()
            gamelist.append(game)

    cardlist = [1]*len(gamelist)
    print(len(cardlist))
    #print (cardlist)

    for game in gamelist:
        add = game.get_totmatch()
        to_add = cardlist[int(game.gamenum)-1]
        for i in range(add):
            index = (int(game.gamenum) ) + i
            if index <= 202:
                cardlist[index] += to_add
        print(cardlist)
        
    for cnt in cardlist:
        totscore += cnt
    print(totscore)


if __name__ == "__main__":
    main()
