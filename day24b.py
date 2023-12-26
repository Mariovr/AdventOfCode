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
from decimal import * #to work with high precision numbers

#Run in python (faster as pypy)
def cal_x_z(vx , vz , p1, v1 , p2,v2):
    try:
        a = Decimal(1.)/(v1[0] - vx)
        b = -p1[0]/(v1[0] - vx)
        c = Decimal(1.)/(v1[2]-vz)
        d = -p1[2]/(v1[2] - vz)
        a2 = Decimal(1.)/(v2[0] - vx)
        b2 = -p2[0]/(v2[0] - vx)
        c2 = Decimal(1.)/(v2[2]-vz)
        d2 = -p2[2]/(v2[2] - vz)
        x= (c*b2/c2 - c *d2/c2 + d - b )*Decimal(1.)/(a-c*a2/c2)
        z = (a2 *x + b2 -d2)/c2
        return x, z
    except ZeroDivisionError:
        return None, None

def cal_y(x ,vx, vy , p1, v1):
    try:
        y = (x - p1[0])/(v1[0] - vx) * (v1[1] - vy) + p1[1]
        return y
    except ZeroDivisionError:
        return None

def intersec(pvec1 , pvec2 , vvec1 , vvec2):
    t1,t2,t3 = (0,0,0)
    if vvec1[0] != vvec2[0]:
        t1 = (pvec2[0] - pvec1[0])/(vvec1[0]-vvec2[0])
    if vvec1[1] != vvec2[1]:
        t2 = (pvec2[1] - pvec1[1])/(vvec1[1]-vvec2[1])
    if vvec1[2] != vvec2[2]:
        t3 = (pvec2[2] - pvec1[2])/(vvec1[2]-vvec2[2])
    times = [t1,t2,t3]
    zerot = [ind  for ind, t in enumerate(times) if t ==0 ]
    nzerot = [t for t in times if t !=0 ]
    for ind in zerot:
        times[ind] = nzerot[0]
    return times

#def get_xr(zr):
#    return (307351257536384. - (182308577450321.-zr)/ ( 349260476816766-zr)*285213989112104) *(1./(1.-1*(182308577450321-zr)/(349260476816766-zr) ) )

#Two hails with same x and z speed, gave an easy relation to speed up things a bit.
#paths with same x and z velocity.
#285213989112104, 158755554306260, 349260476816766 @ -39, 7, 14
#307351257536384, 449879793266828, 182308577450321 @ -39, -419, 14
def get_vzr(vx):
    return (vx+39.) *(182308577450321. - 349260476816766)/(307351257536384.-285213989112104) + 14.

def main(args , **kwargs):
    haillist = []
    for line in args:
        pos,vel= line.split('@')
        pvec = [Decimal(p) for p in pos.split(',') ]
        vvec = [Decimal(v) for v in vel.split(',') ]
        haillist.append((pvec,vvec))

    #rockpos = [24,13,10] #to test intersection method on sample problem.
    #rockvel = [-3,1,2]   #to test intersection method on sample problem.
    #Speeds of all the hails are quite low but go in all directions, so its reasonable to assume vx and vy of rock will also not be to large, to brute force v (instead of using a symbolic equation solver, we can use pure python).
    for vx in range(-500,500):
        if vx % 20 == 0:
            print('Vtest: ' , vx)
        for vy in range(-500,500):
            vz = Decimal(get_vzr(vx))
            rockvel =[Decimal(vx) ,Decimal(vy) , Decimal(vz)] 
            x , z = cal_x_z(vx, vz , haillist[0][0] , haillist[0][1] , haillist[1][0] , haillist[1][1])
            if x == None:
                continue
            y = cal_y(x,vx,vy, haillist[0][0] , haillist[0][1] )
            if y == None:
                continue
            rockpos = [x,y,z]
            good = True
            for index, hail in enumerate(haillist):
                t1,t2,t3 = intersec(hail[0], rockpos, hail[1], rockvel)
                if t1 >= 0  and t2 >=0 and t3>= 0 and round(t1,1) == round(t2,1) == round(t3,1):
                    #xc = hail[1][0] * t1 + hail[0][0]
                    #yc = hail[1][1] * t2 + hail[0][1]
                    #zc = hail[1][2] * t3 + hail[0][2]
                    ##print('Pos cross: ' , xc,yc,zc)
                    if index >1:
                        print('Intersection at index: ', index, ' times: ' , t1,t2,t3)
                else:
                    #print('tf', t1,t2,t3)
                    good = False
                    break
            if good: #if collided with all hails.
                break
        if good:
            break

#To check for Easy relationships.
#    for ind, hail in enumerate(haillist):
#        for ind2,hail2 in enumerate(haillist[ind+1:]):
#            if hail[1][0] ==  hail2[1][0]:
#                #if hail[1][0] ==  hail2[1][0]:
#                print('same vel x: ' , hail[1][0] , ' at x' , hail[0][0] , hail2[0][0] , hail2[0][0] - hail[0][0], 'at indexes:' , ind,ind2)

    print('Rockpos: ' , rockpos)
    print('Rockvel: ' , rockvel)
    return sum(rockpos)

if __name__ == "__main__":
    stringlist ="""19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
"""

#    lines = [line.strip() for line in stringlist.strip().split('\n')]
#    print(lines)
#    assert main(lines) == 47
#
    file = "inputday24.txt"
    with open(file,'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    result = main(lines)
    print('Result is: ', result)

