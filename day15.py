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


def cal_val( string):
    val = 0
    for i in string:
        val += ord(i)
        val *= 17
        val = val %256
    return val

def cal_valb(boxes):
    val = 0
    for index, box in enumerate(boxes):
        for ind, lens in enumerate(box):
            if lens != '':
                val += (index+1) * (ind+1) * int(lens[1])
    return val

def add_lens(boxes, string):
    boxnum = cal_val(string[:string.index('=')])
    action = string.split('=')
    if boxes[boxnum] != [''] and action[0] in [ act[0] for act in boxes[boxnum] ] :
        index = [ act[0] for act in boxes[boxnum] ].index(action[0])
        boxes[boxnum][index]  = action
    else:
        if boxes[boxnum] != ['']:
            boxes[boxnum].append(action)
        else:
            boxes[boxnum][0] = action


def remove_lens(boxes, string):
    boxnum = cal_val(string[:string.index('-')])
    action = string.split('-')
    if boxes[boxnum] != [''] and action[0] in [ act[0] for act in boxes[boxnum] ] :
        index = [ act[0] for act in boxes[boxnum] ].index(action[0])
        del boxes[boxnum][index]  
    else:
        pass

def main(*args , **kwargs):
    maplist = []
    val = 0
    string ='rn=1'
    file = "inputday15.txt"
    lines = []
    result = 0
    with open(file,'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    #lines = 'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'
    lines = lines[0].split(',')
    #lines = lines.split(',')
    for string in lines:
        result += cal_val(string)
    print('result a: ', result)

    boxes = ['']*256
    boxes = [[''] for box in  boxes]
    for string in lines:
        if '-' in string:
            remove_lens(boxes, string)
        else:
            add_lens(boxes,string)

    #print(boxes)
    result = cal_valb(boxes)
    print('result b: ', result)
    
    return result

if __name__ == "__main__":
    main()



