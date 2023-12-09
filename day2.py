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

    def __init__(self,game_id , limits):

        self.gameid = game_id
        self.limits = limits
        self.keys = ['red','blue','green']

        self.sample_list = []
        self.validgame = True

        self.minset = {'red' :  0  , 'blue' : 0 , 'green':0}
        self.powerminset = 0

    def add_sample(self, sampdict):
        for key in self.keys:
            if key not in sampdict.keys():
                sampdict[key] = 0
        for key in sampdict.keys():
            if key not in self.keys:
                print('Incorrect key in input ' + key)
                sys.exit(1)

        self.sample_list.append(sampdict)
        self.valid_game()

    def set_min_set(self):
        for key in self.minset.keys():
            for sample in self.sample_list:
                if self.minset[key] < sample[key]:
                    self.minset[key] = sample[key]

        self.powerminset = reduce(lambda x, y: x*y, self.minset.values())


    def valid_game(self):

        for sample in self.sample_list:
            for key in self.keys: 
                if sample[key] > self.limits[key]:
                    self.validgame = False

    def __str__(self):
        outputstr = 'Game object with id: ' + str(self.gameid) + '\n'
        outputstr += '-------------------------------------\n'
        outputstr +='The limits are: ' + str( self.limits) + '\n'
        outputstr +='The samples: \n'
        outputstr +=str(self.sample_list)
        outputstr +='Its a valid game: ' + str( self.gameid) + '\n'
        return outputstr


def main(*args , **kwargs):
    file = "inputday2.txt"
    limit = {'red' : 12 , 'green' : 13 , 'blue' : 14}
    gamelist = []

    with open(file,'r') as f:
        for line in f:
            game_id = int(re.search(r'Game\s*(\d+)' , line).group(1))
            game = Game(game_id, limit)

            samplelist = re.findall(r'(((\s*\d+\s*\w+)(?=,*))+(?=;|$))',line)
            samplelist = re.findall(r'(((\s*\d+\s*\w+),*)+(?=;|$))',line)
            for tup in samplelist:
                numlist = re.findall(r'\d+',tup[0])
                numlist = [int(num) for num in numlist]
                collist = re.findall(r'[a-zA-Z]+',tup[0])
                sample = dict(zip(collist,numlist))
                game.add_sample(sample)

            print(game)
            game.set_min_set()
            gamelist.append(game)


    result = 0
    minsettot = 0
    for game in gamelist:
        if game.validgame:
            result += game.gameid
    print('Final result: ' , result)

    for game in gamelist:
        minsettot += game.powerminset 
    print('Final result minsettot: ' ,minsettot)



if __name__ == "__main__":
    main()


