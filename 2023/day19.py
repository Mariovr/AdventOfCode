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

def main(args , **kwargs):
    partlist = []
    ruledict = {}
    properties = ['x','m','a','s']

    result = 0
    accepted = []
    blank = False
    for line in args:
        if not blank and line != '':
            rules = re.findall(r'([xmas])([><])(\d+):(\w+)', line  ) 
            key = re.search(r'(\w+)\{', line  ).group(1)
            fdest = re.search(r',(\w+)\}', line  ).group(1)
            rules += [fdest]
            ruledict[key] = rules
        if blank:
            partlist.append(  list(re.search(r'(\d+),m=(\d+),a=(\d+),s=(\d+)',line).groups()))
        if line == '':
            blank = True
    partdict = [ { p : int(v) for p,v in zip(properties,part)  } for part in partlist]
    for part in partdict:
        currule = 'in'
        notend = True
        #print(part)
        while(notend):
            for rul in ruledict[currule]:
                if type(rul) == str:
                    currule = rul
                else:
                    if rul[1] == '>':
                        if part[rul[0]]  > int(rul[2]):
                            currule = rul[3]
                            break
                    else:
                        if part[rul[0]]  <  int(rul[2]):
                            currule = rul[3]
                            break
            #print(currule)
            if currule == 'A':
                print('Accepted: ' , part)
                accepted.append(part)
                notend = False
            if currule == 'R':
                notend = False
                   
    print(accepted)
    for part in accepted:
        result += sum(part.values())

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

    lines = [line.strip() for line in stringlist.strip().split('\n')]
    assert main(lines) == 19114

    file = "inputday19.txt"
    with open(file,'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    result = main(lines)
    print('Result is: ', result)



