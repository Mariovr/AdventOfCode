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

def main():
    fname =   "inputday1.txt"
    count= 0
    totsum = 0
    digitlist = [("one" , '1'),("two",'2'),("three",'3'),("four",'4'),("five",'5'),("six",'6'),("seven",'7'),("eight",'8'),("nine",'9'),("ten",'10')]
    
    with open(fname, 'r') as file:
      for line in file:
        match = re.search(r'(\d|one|two|three|four|five|six|seven|eight|nine)',line)
        if len(match.group(0)) > 1:
          dig1 =   match.group(0)
          for i in range(9):  
           dig1 =   dig1.replace(digitlist[i][0],digitlist[i][1])
           print(dig1)
        else:
          dig1 = match.group(0)
        #print(dig1)
        match = re.search(r'.*(\d|one|two|three|four|five|six|seven|eight|nine).*?$',line)
        if len(match.group(1)) > 1:
          dig2 =   match.group(1)
          for i in range(9):  
            dig2 =   dig2.replace(digitlist[i][0],digitlist[i][1])
        else:
          dig2 = match.group(1)
        print(dig1 + ' '+ dig2)

        totsum += int(dig1 + dig2 )

       
    print('total non match= ' , count)
    print('total sum= ' , totsum)
    #print (d.header)
    #print (d.data)
    #d.save_data("test_save2.txt")


if __name__ == "__main__":
    main()
