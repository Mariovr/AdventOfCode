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

import os
import sys
import re

def answer1(rules, pages):
    result = 0
    for pagel in pages:
        if test_good(rules, pagel):
            index = int((len(pagel))/2)
            result += pagel[index]
    print('Result 1: ' , result)

def test_good(rules ,pagel):
    goodOrder = True
    for index, page in enumerate(pagel):
        test = pagel[:index]
        for p in test:
            if page in rules and p in rules[page]:
                goodOrder = False
        if goodOrder == False:
            break
    return goodOrder

def main(args , **kwargs):
    result = 0
    rules ={}
    pages = []
    for line in args:
        if line.find('|') > 0:
            bef, after = [int(i) for i in line.split('|')]
            if bef in rules:
                rules[bef].append(after)
            else:
                rules[bef] = [after]
        if line.find(',') > 0 :
            pages.append([int(i) for i in line.split(',')] )

    answer1(rules, pages)

    corpages = []
    for pagel in pages:
        goodOrder = True
        for index, page in enumerate(pagel):
            test = pagel[:index]
            for ind, p in enumerate(test):
                if page in rules and p in rules[page]:
                    pagel.remove(page)
                    pagel = pagel[:ind] + [page] + pagel[ind:]
                    goodOrder = False
                    break
        if goodOrder == False:
            corpages.append(pagel)

    for pagel in corpages:
        goodOrder = True
        for index, page in enumerate(pagel):
            test = pagel[:index]
            for ind, p in enumerate(test):
                if page in rules and p in rules[page]:
                    pagel.remove(page)
                    pagel = pagel[:ind] + [page] + pagel[ind:]
                    goodOrder = False
                    break
        index = int((len(pagel))/2)
        result += pagel[index]
    print('Result 2: ' , result)

    return result


if __name__ == "__main__":
    stringlist ="""47|53
    97|13
    97|61
    97|47
    75|29
    61|13
    75|53
    29|13
    97|29
    53|29
    61|53
    97|53
    61|29
    47|13
    75|47
    97|75
    47|61
    75|61
    47|29
    75|13
    53|13

    75,47,61,53,29
    97,61,53,29,13
    75,29,13
    75,97,47,61,53
    61,13,29
    97,13,75,29,47
"""

    lines = [line.strip() for line in stringlist.strip().split('\n')]
    print(lines)
    assert main(lines) == 123

    file = "input5.txt"
    with open(file,'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    result = main(lines)
    #print('Result is: ', result)



