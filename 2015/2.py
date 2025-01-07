from aoc import AOC
import re

aoc = AOC(2,  2015 )

input = aoc.input.strip().split('\n')
print(input)
#input = aoc.get_example(0).strip().split('\n')

def part1():
    res = 0
    for line in input:
        l,w,h = map(int, re.findall(r'\d+', line))
        res+= 2* l * w + 2 * w *h + 2*h*l  + min(l * w ,h*l ,w*h)
    return res
    

def part2():
    res = 0
    for line in input:
        l,w,h = map(int, re.findall(r'\d+', line))
        d = sorted([l,w,h])
        res+= l * w *h  + d[0]*2 +   d[1] *2
    return res

    
    return 0

p1_sol = part1()
p2_sol = part2()

# Submit
print('Part 1:', p1_sol)
#aoc.submit(1, p1_sol)
print('Part 2:', p2_sol)
#aoc.submit(2, p2_sol)
