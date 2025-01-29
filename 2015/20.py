# This program is free software. It comes without any warranty, to the extent
# permitted by applicable law. You may use it, redistribute it and/or modify
# it, in whole or in part, provided that you do so at your own risk and do not
# hold the developers or copyright holders liable for any claim, damages, or
# other liabilities arising in connection with the software.
# 
#Developed by Mario Van Raemdonck, 2025;
#
# -*- coding: utf-8 -*-
#! /usr/bin/env python 
from functools import reduce

target = 34000000
res1, res2 = 0,0
for n in range(100000,100000000, 1):
    facs = list(set(reduce( list.__add__, ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0))))
    t1 = sum(facs)*10
    t2 = sum([j for j in facs if n // j <= 50])*11
    if n % 1000 ==0:
        print(n, t1,t2)
    if t2 >= target and res2 == 0:
        res2 = n
    if t1 >= target and res1 == 0:
        res1 = n
    if res1 != 0 and res2 != 0:
        break

print('Result 1:', res1)
print('Result 2:', res2)
