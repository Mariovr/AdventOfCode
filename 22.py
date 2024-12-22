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
with open('input22.txt','r') as aoc:
    text = aoc.read()
inpa = text.strip().split('\n')
stringlist ="""1
2
3
2024
"""
#inpa = [line.strip() for line in stringlist.strip().split('\n')]
print(inpa)

def create_new_sec(val):
    val = (64*val) ^ val
    val = val % 16777216
    val =  (val//32) ^ val
    val =  (val) % 16777216
    val =  (val*2048) ^ val
    val =   val % 16777216
    return val

def find_sell_p(seql, optseq):
    for i in range(0,len(seql)-3,1):
        if [dif   for dif , p in seql[i:i+4]] == optseq:
            print('found:' , seql[i+3][1], 'at pos: ' , i)
            return seql[i+3][1] 
        else:
            continue
    return 0

def find_p_map(seql):
    pmap = {}
    for i in range(0,len(seql)-3,1):
        if [dif   for dif , p in seql[i:i+4]] not in [list(key) for key in pmap.keys()]: #only first occurence of a difference sequence is relevant
            pmap[tuple(dif   for dif , p in seql[i:i+4])] = seql[i+3][1]
    return pmap

def parts():
    res1,res2 = 0,0
    mapl = []
    for i, line in enumerate(inpa):
        val = int(line)
        seql = [val % 10]
        #optseq = [2, -2,4,0] #to check correct optimum sequence list.
        for j in range(2000):
            val = create_new_sec(val)
            price = val%10
            seql.append(price)
        res1 += val
        difl = [(b -a , b) for a,b in zip(seql , seql[1:]) ]
        #res += find_sell_p(difl , optseq) #to check correct optimum sequence list.
        maxp = find_p_map(difl)
        mapl.append(maxp)
    #print('result with optseq:' , optseq, res) #to check correct optimum sequence list

    res2 =0
    for a in range(-6 , 7 , 1):
        for b in range(-6 , 7 , 1):
            for c in range(-6 , 7 , 1):
                for d in range(-6 , 7 , 1):
                    res = 0
                    for pmap in mapl:
                        if (a,b,c,d) in pmap:
                            res += pmap[(a,b,c,d)]
                    if res > res2:
                        print('new max res: ' , res)
                        print('for a b c d: ' , a , b, c, d)
                        res2 = res
    return res1 , res2

result1,result2 = parts()
print('Result 1:', result1)
print('Result 2:', result2)

