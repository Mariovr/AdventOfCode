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
    for j, tup in enumerate([(int(args[0][i]) , int(args[0][i+1])) for i in range(0,len(args[0])-1,2) ]):
        for n in range(tup[0]):
            newstr.append(j) 
        for m in range(tup[1]):
            newstr.append('.')

    revstring = [i for i in reversed(newstr) ]
    breakreach = False
    for i in revstring:
        if '.' not in  newstr:
            break
        if i != '.':
            index = newstr.index('.')
            newstr = newstr[:index] + [i] + newstr[index+1:len(newstr) ]
        newstr = newstr[:-1]
    result = 0
    for i, num in enumerate(newstr):
        result += i* int(num)
    return result

if __name__ == "__main__":
    stringlist ="""2333133121414131402
"""

    lines = [line.strip() for line in stringlist.strip().split('\n')]
    print(lines)
    assert main(lines) == 1928

    file = "input9.txt"
    with open(file,'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    result = main(lines)
    print('Result is: ', result)



