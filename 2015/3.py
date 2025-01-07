import sys
sys.setrecursionlimit(99999999)
from collections import Counter, defaultdict, deque
from copy import deepcopy
from functools import cache
import re
import heapq
from aoc import AOC

aoc = AOC(3 , 2015)
input = aoc.input.strip().split('\n')
stringlist ="""
"""
#input = [line.strip() for line in stringlist.strip().split('\n')]
print(input)

steps = [[0, 1], [1, 0], [0, -1], [-1, 0]]
stepsa = [[1, 1], [-1, -1], [1, -1], [-1, 1]] + steps

class Game(object):
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return (self.value) == (other.value)

    def __str__(self):
        outputstr = 'Value: ' + str(self.value) + '\n'
        return outputstr

@cache
def test():
    pass

def part1():
    result = 0
    dimx = len(input)
    dimy = len(input[0])
    dmap = set()
    x , y = 0,0
    dmap.add((x,y))
    for i, c in enumerate(list(input[0])):
        if c == '>':
            y += 1
        elif c == '<':
            y -= 1
        if c == '^':
            x += 1
        elif c == 'v':
            x -= 1
        dmap.add((x,y))

    return len(dmap)

def part2():
    result = 0
    dimx = len(input)
    dimy = len(input[0])
    dmap = set()
    x , y = 0,0
    xs , ys = 0,0
    dmap.add((x,y))
    for i, c in enumerate(list(input[0])):
        if i % 2 == 0:
            if c == '>':
                y += 1
            elif c == '<':
                y -= 1
            if c == '^':
                x += 1
            elif c == 'v':
                x -= 1
            dmap.add((x,y))
        else:
            if c == '>':
                ys += 1
            elif c == '<':
                ys -= 1
            if c == '^':
                xs += 1
            elif c == 'v':
                xs -= 1
            dmap.add((xs,ys))
    return len(dmap)

result1 = part1()
result2 = part2()
# Submit
print('Result 1:', result1)
#aoc.submit(1, result1)
print('Result 2:', result2)
#aoc.submit(2, result2)

