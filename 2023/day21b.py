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
import day21

def calc_result(odd , even , n2inf , n4inf, nsqr = 202300):
    #S4QTIP4 = 35082 - odd  #make use of result after 196 steps (it has almost 4 tips and 1 S in all 4 quadrants), but it didnt converge enough it had 9 points to little, therefore its better to use the result after 589 steps, to determine S4QTIP4 as well.
    S4QB4Q = (n4inf - n2inf)/2. - 6*even - 4*odd #make use of the difference between 589 and 327 steps this contains 2* (S4Q + B4Q) + 12 even + 8 odd = res589 - res327
    S4QTIP4 = n4inf - 9 * odd - 16 *even  - 3 * S4QB4Q #make use of result after 589 steps, and the prev. calculated S4QB4Q (it has 4 tips and 1 S in all 4 quadrants)
    res = nsqr**2 * even + (nsqr-1)**2 * odd + S4QTIP4 + (nsqr-1)*S4QB4Q #General formula to predict points after even increments in square space. (e.g. for n = 2 -> 97230, n = 4, 314556, ....).
    return res

def test_c(newc, gmap,e, fy, fx):
    it = gmap[newc] 
    if  it == '.' :
        add = (newc,fy,fx)
        e.add(add)

#('At step: ', 327, 'we have pos occupied: ', 97230) n=2 (new squares reached)
#('At step: ', 589, 'we have pos occupied: ', 314556) n=4 (new squares reached) -> with the difference of this result and the previous even step in square space we can calculate B(4quandrants) + S(4Quadrants). Then we can use the number at n=4 to also get s4qtip4. Then we have all ingredients for a general formula to obtain the occupied positions when reaching even increments in squarespace (as 202300 is even). 
def get_opos_inf(gmap , hdim, vdim, startc = ((0,0),0,0) , numsteps = [327,589]):
    d = set([startc])
    results = []
    for i in range(numsteps[-1]):
        e = set()
        for coord , fy , fx in d:
            for newc in [( (coord[0] + 1) , coord[1]),((coord[0] -1) , coord[1]),(coord[0] , (coord[1]+1)  ),(coord[0], (coord[1]-1)  )]:
                if newc[0] == vdim:
                    test_c((newc[0] % vdim , newc[1]),gmap,e, fy+1,fx)
                elif newc[0] == -1:
                    test_c((newc[0] % vdim , newc[1]),gmap,e, fy-1,fx)
                elif newc[1] == hdim:
                    test_c((newc[0]  , newc[1] %hdim),gmap,e, fy,fx+1)
                elif newc[1] == -1:
                    test_c((newc[0] , newc[1]%hdim),gmap,e, fy,fx-1)
                else:
                    test_c((newc[0] , newc[1]),gmap,e, fy,fx)
        d = e
        if  (((i +1) - 65) % 131) == 0: #at the points where we start a new square (new max fy or fy).
            print('At step: ' , i +1, 'we have pos occupied: ' , len(d))
            if (i+1) in numsteps:
                results.append(len(d))
    return results

#If all pos in a square are reached once it will fluctuate between the odd (reachable) and even (reachable), num of positions in that square (using sol a: 7757 (even) and 7748 (odd).
#start position is in the exact middle coordinates: (65,65) and dimensions of square are (131,131). There are straight paths from start to next squares in all 4 directions (and also diagonally).
#So surface to consider will be a square of 26501365 size in all directions. It will contain many full squares, 4 tips, and then interchanging small and big parts of a square.
#After 65 steps we reach the next squares in square space. After 65 + 131 = 196 again the next squares with new max/min in square coordinate space, and so on...
#26501365 = 65 + 131 * 202300. 
#(y,x, field vert,field hor)
def main(args , **kwargs):
    gmap = {}
    numstep =  26501365
    vdim = len(args)
    hdim = len(args[0])

    startc = (0,0, 0 , 0)
    for ind , line in enumerate(args):
        sp = re.search(r'S' , line)
        if sp:
            startc = ((ind , sp.start()) , 0 , 0)
        gmap.update( {(ind,i):ch for i,ch in enumerate(line)} )
    gmap[startc[0]] = '.'

    n_even = day21.get_opos(gmap, startc[0] , 160) 
    n_odd = day21.get_opos(gmap,startc[0] , 161)
    print('Even and odd number of converged positions in one square: ', n_even, n_odd)

    nsquar_reached = (numstep - (startc[0][0] )) / hdim
    print('nsquare reached after ' , numstep, ' nsquare reached: ' , nsquar_reached)

    ressteps = [startc[0][0] + 2*hdim, startc[0][0] + 4*hdim]
    infres = get_opos_inf( gmap, hdim, vdim, startc, ressteps )
    print('Infinite info at even number (2 and 4) of new squares reached: ', infres )
    for i in (2,4,6,8,10): #To check that the results obtained by the formula are equal to the ones obtained with the get_opos_inf function.
        print('Result at ' , i , ' squares reached: ' , calc_result(n_odd , n_even , infres[0] , infres[1], i) )
    res = calc_result(n_odd , n_even , infres[0] , infres[1], nsquar_reached)
    return res

if __name__ == "__main__":
    file = "inputday21.txt"
    with open(file,'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    result = main(lines)
    print('Result is: ', result)


