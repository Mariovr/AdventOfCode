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

def calc_antin(loc, dimx , dimy, p2 = False):
    antinodes = set()
    for let in loc.keys():
        for i, node in enumerate(loc[let]):
            for node2 in loc[let][i+1:]:
                if p2:
                    antinodes.add((node[0] , node[1]  ) )
                    antinodes.add((node2[0] , node2[1]  ) )
                stepx = node[0] - node2[0]
                stepy = node[1] - node2[1]
                i = 1
                while (stepx != 0 or stepy != 0) and (0 <= node[0] + stepx*i < dimx ) and (0<= node[1] + stepy*i < dimy):
                    antinodes.add((node[0] + stepx*i, node[1] + stepy*i ) )
                    i += 1
                    if not p2:
                        i = 100
                stepx *=  -1
                stepy *=  -1
                i = 1
                while (stepx != 0 or stepy != 0) and (0 <= node2[0] + stepx*i < dimx ) and (0<= node2[1] + stepy*i < dimy):
                    antinodes.add((node2[0] + stepx*i, node2[1] + stepy*i ) )
                    i += 1
                    if not p2:
                        i = 100
    return len(antinodes)

def main(args , **kwargs):
    locations = {}
    for i , line in enumerate(args):
        print (line)
        for j , let in enumerate(line):
            if let != '.':
                if let in locations:
                    locations[let].append((i,j))
                else:
                    locations[let] = [(i,j)] 

    print('Part 1: ' , calc_antin(locations , len(args), len(args[0]) ) )
    print('Part 2: ' , calc_antin(locations , len(args), len(args[0]) , True) )

if __name__ == "__main__":
    file = "input8.txt"
    with open(file,'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
        main(lines)

