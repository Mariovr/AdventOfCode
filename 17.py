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
import re
import sys
from aoc import AOC

aoc = AOC(17 , 2024)
inpa , inpb = aoc.input.strip().split('\n\n')
nums = lambda s : [int(x) for x in re.findall(r'-?\d+', s)]

def get_output(rega , operations):
    #operations is a list of tuples containing (instructions, operands)
    regs = [rega , 0 , 0 ]
    output = []
    ops = {0 : 0 , 1:1 , 2:2 , 3  : 3, 4:regs[0] , 5:regs[1] , 6 : regs[2]}
    inrd = 0
    while( inrd < len(operations)):
        inr , opc = operations[inrd][0] , operations[inrd][1]
        if inr == 0 :
            regs[0] = regs[0] // 2**ops[opc]
            ops[4] = regs[0]
        elif inr ==1:
            regs[1] =  regs[1] ^ opc
            ops[5] = regs[1]
        elif inr == 2:
            regs[1] = ops[opc] %8
            ops[5] = regs[1]
        elif inr == 3:
            if regs[0] ==0:
                inrd += 1
                continue
            else:
                inrd = opc//2
                inrd -= 1
        elif inr == 4 :
            regs[1] =  regs[1] ^ regs[2]
            ops[5] = regs[1]
        elif inr == 5:
            output.append(ops[opc] %8)
        elif inr == 6:
            regs[1] = regs[0] // 2**ops[opc]
            ops[5] = regs[1]
        elif inr == 7:
            regs[2] = regs[0] // 2**ops[opc]
            ops[6] = regs[2]
        inrd +=1
    return output

def parts():
    regs = [ nums(reg)[0] for reg in inpa.split('\n')]
    ope = nums(inpb)
    ext= [(a,b) for a,b in zip(ope[::2] , ope[1::2])]
    res1 = ','.join([str(i) for i in get_output(regs[0], ext)] )
    """The program executes 8 steps: 1     2     3     4     5     6     7     8
                                   (2,4),(1,2),(7,5),(0,3),(4,7),(1,7),(5,5),(3,0)
                                   B=A%8 swap   C =   A/8   swap swaps  W B%8 go to start 
                                         bit   A/2**B       bits l 3b         until A =0
                                         2 of               of B  ofB 
                                         B                  where 
                                                            C has1
    -> only B modulo 8 gets written every execution.
    -> no memory of B nor C is required between executions, as they get re-initiated every execution, only A keeps changing (division by 8)
    -> all instructions get executed every execution from start to end
    -> Every execution: A gets divided by 8 until it becomes zero, then next execution will be the last. For part 2 we need to print 16 characters -> the number we search is of the form 8**15*a + 8**14*b + ... + 8 * o + p
    -> Step 3 complicates things, as its the only step that requires more info of A than its modulo 8 number, otherwise we just had to run the program with inputs 0 till 7, check what the output is for each number
       and then fill in the form: 8**15*a + 8**14*b + ... + 8 * o + p, in reverse order: a should be input linked to 0, b input linked to 3, ..., p input linked to 2. So we need to find the 16 vars from a till p.
    -> But as B is between 0 - 7, and C later is only used to swap bits of B, only the space A % 2**7 *8 = 1024 = 2 * 8**3 is relevant, and can influence a given number.
    -> Therefore we can in one go find from the first 4 powers of 8 their associated factors, by trying all combinations (a,b,c,d) until they output the last 4 digits of the program: 5530, and set the other factors to a random value
       Then set the factors of the 4 found variables, and then loop over all next two variables until the last 6 digits  of the program are equal, then set the 6 factors, and find the next two.
    -> Until we found enough factors so we can scan completely the remaining part until the output and program list are equal. 
    -> I guess above flow can be automated, but its how I found the solution :p, scanning the output and gradually filling factors, in reverse order of output.
    """
    for j in range(0, 8**7):
    #for b in range(0,8):
        #for a in range(1,8):
            #i = 8**15*5 + 8**14*3+8**13*2+8**12*2+8**11*a+8**10*b
            #print(a,b)
        i = 8**15*5 + 8**14*3+8**13*2+8**12*2+8**11*3+8**10*5+8**9*0+8**8 +8**7 * 3 + 8**6 * 4 + j
        output = get_output(i , ext)
        if output == ope:
            print(output)
            break
    #       if output[-6:] == ope[-6:]: 
    #           print('found -2 factors:')
    #           print(a,b)
    #           print(output)
    return res1, i

result1, result2 = parts()
print('Result 1:', result1)
print('Result 2:', result2)
# Submit
#aoc.submit(1, result1)
#aoc.submit(2, result2)
