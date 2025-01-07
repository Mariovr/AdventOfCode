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

import re
import sys
from math import lcm

#high pulse is 1, low pulse is 0 
class Tool(object):
    def __init__(self, label , destinations):
        self.label = label
        self.lsent = 0
        self.hsent = 0
        self.destinations = destinations
        self.nums = len(self.destinations)

    def __str__(self):
        outputstr = 'Label: ' + str(self.label) + '\n'
        outputstr += 'lsent: ' + str(self.lsent) + '\n'
        outputstr += 'hsent: ' + str(self.hsent) + '\n'
        outputstr += 'Destinations: ' + str(self.destinations) + '\n'
        return outputstr

class Switch(Tool):
    def __init__(self, label , destinations, status = 0):
        super(Switch,self).__init__(label,destinations)
        self.status = status

    def pulse(self, pulse = 0, slabel = ''):
        #print('self label : ' , self.label)
        if pulse:
            return None,self.destinations, self.label
        else:
            self.status = (self.status+ 1) % 2
            if self.status: 
                self.hsent += 1 * self.nums
                return 1, self.destinations, self.label
            else:
                self.lsent += 1 * self.nums
                return 0, self.destinations, self.label

    def __str__(self):
        outputstr = super(Switch,self).__str__()
        outputstr += 'Status: ' + str(self.status) + '\n'
        return outputstr

class Conjunction(Tool):
    def __init__(self, label, destinations, inputs = {}):
        super(Conjunction,self).__init__(label,destinations)
        self.inputs = inputs

    def pulse(self, pulse = 0, slabel = ''):
        self.inputs[slabel] = pulse
        #print('inverted: ' , self.inputs.items() )
        if 0 not in self.inputs.values():
            self.lsent += self.nums
            return 0, self.destinations, self.label
        else:
            self.hsent += self.nums
            return 1, self.destinations, self.label

    def __str__(self):
        outputstr = super(Conjunction,self).__str__()
        outputstr += 'Inputs: ' + str(self.inputs) + '\n'
        return outputstr

class Broadcaster(Tool):
    def __init__(self, label, destinations, inputs = {}):
        super(Broadcaster,self).__init__(label,destinations)

    def pulse(self, pulse = 0, slabel = ''):
        if pulse:
            self.hsent += self.nums +1 #to account for the button push (1 low) and the low sent to all destinations
        else:
            self.lsent += self.nums  + 1
        return pulse, self.destinations, self.label

def init_conjs(rdict):
    for conj in (conj for conj in rdict.values() if isinstance(conj, Conjunction)):
        inp = {}
        #print(conj)
        ilab = [ dest.label for dest in rdict.values() if conj.label in dest.destinations ]
        conj.inputs = dict(zip(ilab,[0] * len(ilab) )) #initialise all to zero.

def apply_rule(rdict, label, pulse, slabel):
    return rdict[label].pulse(pulse, slabel) 

def main(args , **kwargs):
    rdict = {}
    result = 0
    for line in args:
        rule = re.search(r'([%&]*)(\w+)\s*->\s*([\s*\w+,]*\w*)', line  ) 
        dest = [rul.strip() for rul in rule.group(3).split(',')]
        if rule[1] == '%':
            rdict[rule[2]] =  Switch(rule[2], dest)
        elif rule[1] == '&':
            rdict[rule[2].strip()] = Conjunction(rule[2], dest)
        else:
            rdict['broadcaster'] = Broadcaster('broadcaster', dest)

    init_conjs(rdict)

    #For solution A just set the range to 1000.
    for i in range(100000000000):
        pulse ,dest,olabel = apply_rule(rdict, 'broadcaster', 0 ,'button')
        actions = list(zip([pulse] * len(dest) , dest , [olabel]* len(dest) ) )
        #print(actions)
        while(len(actions)):
            nactions = []
            for p, d, l in actions:
                newp , newd, slab = apply_rule(rdict, d , p, l)
                #For solution B, to trigger rx, we see that it gets triggered by the conjunction lx
                #So lx will sent a low, when all its inputs have sent a high in the same iteration.
                #The inputs are: cl,rp,lb,nj. These are also all conjunctions, so they will sent a high, when they have received a low.
                #So we just let the loop run and observe the periods of when these 4 conjunctions sent a high, we can then estimate when they will all collide.
                #We are again lucky that the period starts immediately and there is no warmup in contrast with day 14, where the period only started after some cycles.
                #So we can again use the lowest common multiple, instead of more advanced calculations. 
                if  newp == 0 and ('cl' in newd or 'rp' in newd or 'lb' in newd or 'nj' in newd):
                    print('lx received high at index: ' , i+1 , ' for ' , newd)
                if newp is not None: 
                    for des in newd:
                        if des in rdict.keys():
                            nactions.append(  (newp,des, slab) )
            actions = nactions
            #print(actions)

    lval = sum([it.lsent for  it in rdict.values() ] )
    hval = sum([it.hsent for  it in rdict.values() ] )
    result = lval*hval
    print('Result a is: ', result , ' dont forget to put the iterations back to 1000 for answer a')
    return result

if __name__ == "__main__":
    stringlist ="""broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
"""
    stringlist = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
"""

#    lines = [line.strip() for line in stringlist.strip().split('\n')]
#    print(lines)
#    assert main(lines) == 11687500
#
    file = "inputday20.txt"
    with open(file,'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    result = main(lines)
    print('Result is: ', result)

