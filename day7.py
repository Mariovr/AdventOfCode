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


class Hand(object):

    def __init__(self, hand , bid):

        self.hand = hand
        self.bid = int(bid)
        self.type = 0
        self.num = 0
        self.det_type()
        self.det_num()
        self.rank = 0

    def det_type(self):
        self.all_freq = {}
        for i in self.hand:
            if i in self.all_freq:
                self.all_freq[i] += 1
            else:
                self.all_freq[i] = 1
 
       
        if 5 in self.all_freq.values():
            self.type = 6
            return

        if 4 in self.all_freq.values():
            self.type = 5
            return

        if 3 in self.all_freq.values():
            if 2 in self.all_freq.values():
                self.type = 4
                return
            else:
                self.type = 3
                return

        d = [i for i in self.all_freq.values() if i == 2]
        if len(d) == 2:
            self.type = 2
            return
        elif len(d) == 1: 
            self.type =1
            return
        else:
            self.type = 0
            return

    def det_num(self):
        for index, h in enumerate(self.hand):
            if h == 'A':
                self.num += 14 * (14**(5-index))
            elif h == 'K':
                self.num += 13 * (14**(5-index))
            elif h == 'Q':
                self.num += 12 * (14**(5-index))
            elif h == 'J':
                self.num += 11 * (14**(5-index))
            elif h == 'T':
                self.num += 10 * (14**(5-index))
            else:
                self.num += int(h) * (14**(5-index))

    def __str__(self):
        outputstr = 'hand: ' + str(self.hand) + '\n'
        outputstr += 'bid: ' + str(self.bid) + '\n'
        outputstr += 'bid: ' + str(self.rank) + '\n'
        outputstr += 'type: ' + str(self.type) + '\n'
        outputstr += 'num: ' + str(self.num) + '\n'
        return outputstr


def main(*args , **kwargs):
    file = "inputday7.txt"
    hanlist = []

    with open(file,'r') as f:
        for line in f:
            info = re.findall(r'\w+', line)
            han = Hand(info[0],info[1])
            hanlist.append(han)

    hanlist.sort(key= lambda x :  x.type * 14**7 + x.num)
    wins = 0
    for index, han in enumerate(hanlist):
        wins += (index+1) * han.bid
        print(han)
    print('wins: ' , wins)


if __name__ == "__main__":
    main()
