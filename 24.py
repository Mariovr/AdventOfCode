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
import sys
sys.setrecursionlimit(9999)
from copy import deepcopy
from aoc import AOC

aoc = AOC(24 , 2024)
inpa , inpb = aoc.input.strip().split('\n\n')
inpa = [a.strip() for a in inpa.split('\n')]
inpb = [b.strip() for b in inpb.split('\n')]

#bitl = [(number >> bit) & 1 for bit in range(num_bits - 1, -1, -1)] 
#'{0:08b}'.format(num)
def get_target(mp):
    xres =''.join([str(xv) for x, xv in sorted(mp.items(), key = lambda x : x[0])  if x.startswith('x' )])
    xres = int(xres[::-1],2)
    yres =''.join([str(yv) for y, yv in sorted(mp.items(), key = lambda x : x[0]) if y.startswith('y')])
    yres = int(yres[::-1],2)
    zres = xres+yres
    print('zlength' , len(bin(zres)[2:]), ' testsum: ' , xres , yres, zres, bin(zres))
    return bin(zres)[2:][::-1]

def test_sum(mp , zl):
    xres =''.join([str(xv) for x, xv in mp.items() if x.startswith('x' )])
    xres = int(xres[::-1],2)
    yres =''.join([str(yv) for y, yv in mp.items() if y.startswith('y')])
    yres = int(yres[::-1],2)
    zres = ''.join([str(zv) for z, zv in zl])
    zres = int(zres[::-1],2)
    print('testsum:' , xres ,' + ' ,  yres, ' = ',  xres+yres , ' and is calculated as: ' , zres)
    assert xres + yres == zres

def swap(mp , x , y):
    save = mp[x] 
    mp[x] = mp[y] 
    mp[y] = save

def find(val,mp , opem):
    if val in mp:
        return mp[val]
    elif opem[val][0] in mp and opem[val][1] in mp:
        res = opem[val][2](mp[opem[val][0]], mp[opem[val][1]])
        mp[val] = res
        return res
    else:
        try:
            res1 = find(opem[val][0], mp , opem)
            res2 = find(opem[val][1], mp , opem)
            res = opem[val][2](res1, res2)
            mp[val] = res
        except RecursionError:
            return RecursionError
        return res

def fill_zl(zl,mp , opem):
    for i, z in enumerate(zl):
        zv = find(z[0], mp , opem )
        if zv is RecursionError:
            return RecursionError
        zl[i]= (z[0], zv)
    res = ''.join([str(zv) for z, zv in zl])
    return res

def parts():
    opd = {'AND' : lambda x,y: x and y, 'OR' : lambda x,y : x or y, 'XOR' : lambda x, y: x ^ y}
    mp = {}
    for i, line in enumerate(inpa):
        vals = line.split(':')
        mp[vals[0]] = int(vals[1])
    startmp = deepcopy(mp) #to keep im memory the start x and y values

    opem, zl = {}, []
    for  j, line in enumerate(inpb):
        opn = line.split(' ')
        if opn[0] in mp and opn[2] in mp:
            mp[opn[4]] = opd[opn[1]](mp[opn[0]], mp[opn[2]] )
        opem[opn[4]] = (opn[0], opn[2], opd[opn[1]] , opn[1])
        if opn[4].startswith('z'):
            zl.append((opn[4] , -1))
    zl = sorted(zl, key = lambda x : x[0] ) 
    #part 1:
    res1 = fill_zl(zl , mp, opem)
    res1 = int(res1[::-1],2)

    #part 2: za = (xa ^ ya ) ^ (x(a-1) and y(a-1) OR (x(a-1) ^ y(a-1) and xa-2 and ya-2 ) OR go further down ...
    target = [int(l) for l in list(get_target(mp))]
    if len(target) < len(zl):
        target += '0' #in case sum of x and y didnt reach bit 46 (pos 45 in list) we miss the last 0, most significant bits are in the right in current convention.
    first_bad_bit = 0
    for i, z in enumerate(zl):
        if target[i] != z[1]:
            first_bad_bit = i
            break
    print('Start first bad bit: ' , i)
    zswitch = [(k , v) for k , v in sorted(opem.items(), key = lambda x : x[0] ) if k.startswith('z') and v[3] != 'XOR' and k != 'z45'] #because for addition final operation will always be a XOR of the same bit of x and y together with a xor on the history going potentially back to bit zero :p, except for the last z bit so we exclude it. So all the others need to be switched for sure!
    print('zswitch: ' , zswitch)
    swapl = [(k , v) for k , v in sorted(opem.items(), key = lambda x : x[0] ) if not k.startswith('z') and v[3] == 'XOR' and not (v[0].startswith('x') or v[0].startswith('y') )]
    print('zswapl: ' , swapl) #Potential swap candidates for entries in zswitch.
    swap(opem , 'ctg', 'rpb') #solves issue at bit 15, after correcting bit 11, issue appeared at bit 15, then that swap was necessary to bring z15 in the correct pattern: z15 = (xa ^ ya ) ^ (x(a-1) and y(a-1) OR (x(a-1) ^ y(a-1) and xa-2 and ya-2 ) OR go further down
    for zswit in [ k for k, v in zswitch ]:
        for nswap in [ k for k,v in swapl]:
            print('#at following swaps: ' , zswit , nswap)
            goodswap = False
            swap(opem, zswit , nswap)
            mp = deepcopy(startmp)
            res = fill_zl(zl , mp, opem)
            if res is RecursionError:
                continue
            for i, z in enumerate(zl):
                if target[i] != z[1]:
                    if i > first_bad_bit+1 :
                        #print('new best not equal bit at: ' , i)
                        first_bad_bit= i
                        goodswap = True
                    else: #undo bad swap
                        #print('bad bit at: ' , i, ' for swap : ' , zswit , nswap)
                        swap(opem, zswit , nswap)
                        goodswap = False
                    break
                elif i == len(zl)-1:
                    goodswap = True

            if goodswap:
                print('Found good swap: ' , zswit, nswap)
                break

    res2 =  ','.join(sorted([ k for k, v in zswitch ] + [ k for k,v in swapl] + ['ctg','rpb']))

    #maps res onto: x opn y, to get some quick info if we can determine easily some swaps:
    #maps res onto: x opn y 
    xopsand = [(k , v[0] , v[1] , v[3]) for k , v in sorted(opem.items(), key = lambda x : x[1][1] ) if (v[0].startswith('x') or v[1].startswith('x')) and v[3] == 'AND']
    xopsxor = [(k , v[0] , v[1] , v[3]) for k , v in sorted(opem.items(), key = lambda x : x[1][1] ) if (v[0].startswith('x') or v[1].startswith('x')) and v[3] == 'XOR']
    print('XOR operations on x and y have length: ' , len(xopsxor) )
    print(xopsxor)
    print('AND operations on x and y have length: ' , len(xopsand) )
    print(xopsand)
    test_sum(mp ,zl)
    return res1, res2

result1, result2 = parts()
print('Result 1:', result1)
print('Result 2:', result2)

