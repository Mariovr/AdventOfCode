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
import copy

class APart(object):
    def __init__(self, xmin , xmax ,  mmin ,mmax,  amin, amax ,  smin, smax , nxtrule):
        self.ranges = {}
        self.ranges['x' ] = [xmin, xmax]
        self.ranges['m' ] = [mmin , mmax]
        self.ranges['a' ] =  [amin, amax ]
        self.ranges['s' ] = [smin , smax]
        self.nxtrule = nxtrule

    def split_part(self, key , val, index):
        newd = copy.deepcopy(self.ranges)
        newd[key][index] = val
        return APart(newd['x'][0],newd['x'][1],newd['m'][0],newd['m'][1],newd['a'][0],newd['a'][1], newd['s'][0],newd['s'][1], self.nxtrule)

    def __str__(self):
        return 'Nxtrule: ' + self.nxtrule + ' ' + str(self.ranges)

def apply_rule(apart , currule, ruledict):
    splitparts = []
    for rul in ruledict[currule]:
        if type(rul) == str:
            apart.nxtrule = rul
        else:
            if rul[1] == '>':
                spart = apart.split_part(rul[0] ,  int(rul[2])+1 , 0 )
                spart.nxtrule = rul[3]
                apart.ranges[rul[0] ][1] = int(rul[2])
                splitparts.append(spart)
            else:
                spart = apart.split_part(rul[0] ,  int(rul[2])-1 , 1 )
                spart.nxtrule = rul[3]
                apart.ranges[rul[0] ][0] = int(rul[2])
                splitparts.append(spart)

    return apart, splitparts


def main(args , **kwargs):
    ruledict = {}
    properties = ['x','m','a','s']

    result = 0
    accepted = []
    for line in args:
        rules = re.findall(r'([xmas])([><])(\d+):(\w+)', line  ) 
        if rules:
            key = re.search(r'(\w+)\{', line  ).group(1)
            fdest = re.search(r',(\w+)\}', line  ).group(1)
            rules += [fdest]
            ruledict[key] = rules
        else:
            break

    apartlist = [APart(1,4000,1,4000,1,4000,1,4000, 'in')]
    slist = []
    while(len(apartlist)> 0 ):
        apartlist += slist
        slist = []
        dindl = []
        for ind, apart in enumerate(apartlist):
            print(apart)
            apart, spart = apply_rule(apart ,apart.nxtrule, ruledict)
            delindex = []
            for index, part in enumerate(spart):
                if part.nxtrule == 'A':
                    print('Accepted: ' , part)
                    accepted.append(part)
                    delindex.append(index)
                elif part.nxtrule == 'R':
                    print('Rejected: ' , part)
                    delindex.append(index)
            delindex.reverse()
            for index in delindex:
                del spart[index]
            if apart.nxtrule == 'A':
                print('Accepted: ' , part)
                accepted.append(apart)
                dindl.append(ind)
            elif apart.nxtrule == 'R':
                print('Rejected: ' , part)
                dindl.append(ind)
            slist += spart
        dindl.reverse()
        for ind in dindl:
            del apartlist[ind]

    for part in accepted:
        result += (part.ranges['x'][1] - part.ranges['x'][0]+1)*(part.ranges['m'][1] - part.ranges['m'][0]+1)*(part.ranges['a'][1] - part.ranges['a'][0]+1)*(part.ranges['s'][1] - part.ranges['s'][0]+1)

    return result

if __name__ == "__main__":
    stringlist ="""
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""

#    lines = [line.strip() for line in stringlist.strip().split('\n')]
#    assert main(lines) == 167409079868000

    file = "inputday19.txt"
    with open(file,'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    result = main(lines)
    print('Result is: ', result)



