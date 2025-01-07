from aoc import AOC

aoc = AOC(1, 2015  )

input = aoc.input.strip().split('\n')
print(input)

def part1():
    return input[0].count('(')-input[0].count(')') 

def part2():
    nu , nd = 0,0
    for i , c in enumerate(input[0]):
        if c == '(':
            nu += 1
        elif c == ')':
            nd += 1

        if nd > nu:
            return i+1

p1_sol = part1()
p2_sol = part2()

# Submit
print('Part 1:', p1_sol)
#aoc.submit(1, p1_sol)
print('Part 2:', p2_sol)
#aoc.submit(2, p2_sol)
