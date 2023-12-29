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
import sys
import re

#Running the program with a large number of steps, gives for example the following output at important points.
#('At step: ', 196, 'we have pos occupied: ', 35082)  -> with this info we can calculate approx. the number of points in 4tips + 1S (in all 4 quadrants), this will be added to all higher results in square space, but it is 9 points off from the real number as it needed more steps to reach a stable state. 
#('At step: ', 327, 'we have pos occupied: ', 97230)
#('dif', 62148)
#('At step: ', 458, 'we have pos occupied: ', 190388) 
#('dif', 93158)
#('At step: ', 589, 'we have pos occupied: ', 314556) -> with the difference of this result and the previous even step in square space we can calculate B(4quandrants) + S(4Quadrants) (together with odd and even parity of a full square we have all ingredients for our formula, that predicts the number of positions for even increments in squarespace (as 202300 is even). 
#('dif', 124168)
#('At step: ', 720, 'we have pos occupied: ', 469734)
#('dif', 155178)
#('At step: ', 851, 'we have pos occupied: ', 655922)
#('dif', 186188)
#('At step: ', 982, 'we have pos occupied: ', 873120)
#('dif', 217198)
#('At step: ', 1113, 'we have pos occupied: ', 1121328)
#('dif', 248208)
#('At step: ', 1244, 'we have pos occupied: ', 1400546)
#......
def calc_result(odd = 7757, even = 7748,nsqr = 202300):
    #S4QTIP4 = 35082 - odd  #make use of result after 196 steps (it has almost 4 tips and 1 S in all 4 quadrants), but it didnt converge enough it had 9 points to little, therefore its better to use the result after 589 steps, to determine S4QTIP4 as well.
    S4QB4Q = (314556 - 97230)/2. - 6*even - 4*odd #make use of the difference between 589 and 327 steps this contains 2* (S4Q + B4Q) + 12 even + 8 odd = res589 - res327
    S4QTIP4 = 314556 - 9 * odd - 16 *even  - 3 * S4QB4Q #make use of result after 589 steps, and the prev. calculated S4QB4Q (it has 4 tips and 1 S in all 4 quadrants)
    res = nsqr**2 * even + (nsqr-1)**2 * odd + S4QTIP4 + (nsqr-1)*S4QB4Q #General formula to predict points after even increments in square space. (e.g. for n = 2 -> 97230, n = 4, 314556, ....).
    return res


def test_c(newc, gmap,e, fy, fx):
    it = gmap[newc] 
    if  it == '.' :
        add = (newc,fy,fx)
        e.add(add)

#If all pos in a square are reached once it will fluctuate between the odd (reachable) and even (reachable), num of positions in that square (using sol a: 7748 (even) and 7757 (odd).
#start position is in the exact middle coordinates: (65,65) and dimensions of square are (131,131). There are straight paths from start to next squares in all 4 directions (and also diagonally).
#So surface to consider will be a square of 26501365 size in all directions. It will contain many full squares, 4 tips, and then interchanging small and big parts of a square.
#After 65 steps we reach the next squares in square space. After 65 + 131 = 196 again the next squares with new max/min in square coordinate space, and so on...
#26501365 = 65 + 131 * 202300. 
#(y,x, field vert,field hor)
def main(args , **kwargs):
    gmap = {}
    numstep = 5000 
    startc = (0,0, 0 , 0)

    vdim = len(args)
    hdim = len(args[0])
    for ind , line in enumerate(args):
        sp = re.search(r'S' , line)
        if sp:
            startc = ((ind , sp.start()) , 0 , 0)
        gmap.update( {(ind,i):ch for i,ch in enumerate(line)} )

    gmap[startc[0]] = '.'
    d = set([startc])
    print(d)
    savesol = 0
    for i in range(numstep):
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

            #print(e)
        d = e
        if  (((i +1) - 65) % 131) == 0: #at the points where we start a new square (new max fy or fy).
            print('At step: ' , i +1, 'we have pos occupied: ' , len(d))
            print('dif' , len(d) - savesol)
            #print('At step: ' , i + 1 , 'we have max fy: ' , max(d, key = lambda x : x[1]))
            #print('At step: ' , i + 1, 'we have max fx: ' , max(d, key = lambda x : x[2]))
            #print('At step: ' , i + 1, 'we have min fy: ' , min(d, key = lambda x : x[1]))
            #print('At step: ' , i + 1, 'we have min fx: ' , min(d, key = lambda x : x[2]))
            savesol = len(d)

    return 0

if __name__ == "__main__":
    print(calc_result(odd = 7757, even = 7748,nsqr =2))
    print(calc_result(odd = 7757, even = 7748,nsqr =4))
    print(calc_result(odd = 7757, even = 7748,nsqr =6))
    print(calc_result(odd = 7757, even = 7748,nsqr =8))
    res = calc_result()
    print('Result is: ', res)

#    file = "inputday21.txt"
#    with open(file,'r') as f:
#        lines = f.readlines()
#        lines = [line.strip() for line in lines]
#    main(lines)
#
