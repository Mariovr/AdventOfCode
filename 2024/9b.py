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

def main(args , **kwargs):
    newstr = []
    args[0] += str(0)
    pos = 0
    for j, tup in enumerate([(int(args[0][i]) , int(args[0][i+1])) for i in range(0,len(args[0])-1,2) ]):
            newstr.append((j, tup[0], pos, len(newstr)) )
            newstr.append(('.', tup[1], pos + tup[0], len(newstr) )  )
            pos += tup[0] + tup[1]

    revstring = [i for i in reversed(newstr) ]
    for i,il, ipos, d in revstring:
        if i != '.':
            for a, b,c,e in newstr:
                if a == i:
                    index = e
            for p , lp, ppos, nupd in [ tup for tup in newstr[:index] if tup[0] == '.']:
                if lp >= il:
                    newstr = [ (a,b,c,e) if a!= i else ('.' , b,c,e) for a , b, c, e in newstr ]
                    newstr[nupd] = (i,il , ppos, nupd)
                    if lp > il:
                        newstr = newstr[:nupd +1] + [(p, lp-il, ppos + il, nupd +1)] + [ (a,b, c,e+1)  for a,b,c,e in newstr[nupd+1:] ]  
                    break
    result = 0
    for idi , il , ipos , d in newstr:
        if idi != '.':
            for i in range(il):
                result += idi * (ipos + i)
    return result


if __name__ == "__main__":
    stringlist ="""2333133121414131402
"""
    lines = [line.strip() for line in stringlist.strip().split('\n')]
    print(lines)
    assert main(lines) == 2858

    file = "input9.txt"
    with open(file,'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    result = main(lines)
    print('Result is: ', result)

