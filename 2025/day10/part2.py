import sys

from pulp import *

from part1 import parse_input


""" This was an absolutely nightmare for me to solve. I am keeping all
other files/attempts to solve in the repo to possibly come back to but
I struggled so hard with this. I knew a sort of integer solver could do
this but I really really wanted to handle it all myself. After searching
for integer solvers I was able to make this in a half hour.

The overall problem is extremely simple, it's a system of linear equations
problem, but the constraints make it very difficult to achieve. If the
minimum constraint didn't exist it would be as simple as a puzzle could
be but that's the part that is really messing with me. Now that I can
accurately compute each machine's minimum value I can go back and debug
my old trials and see what wasn't working.
"""


def create_matrices(machine) -> tuple[list[list[int]], list[int]]:
    dim = max(len(machine['buttons']), len(machine['joltage']))
    A = [[1 if i in d else 0 for d in machine['buttons']] for i in range(dim)]
    b = list(machine['joltage'] + (0,) * (dim - len(machine['joltage'])))

    return A, b


def solve(A: list[list[int]], b: list[int]) -> list[float]:
    n = len(A[0])
    m = len(A)

    prob = LpProblem('MinSum', LpMinimize)
    x = [LpVariable(f'x{i}', lowBound=0, cat='Integer') for i in range(n)]
    prob += lpSum(x)

    for i in range(m):
        prob += lpSum([A[i][j] * x[j] for j in range(n)]) == b[i]

    prob.solve(PULP_CBC_CMD(msg=0))

    return [value(x[i]) for i in range(n)]


def main(data) -> int:
    total_sum = 0
    for n, machine in enumerate(data):
        A, b = create_matrices(machine)

        result = solve(A, b)

        total_sum += int(sum(result))
    
    return total_sum


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} FILEPATH')
    filepath = sys.argv[1]

    data = parse_input(filepath)
    result = main(data)
    print(f'Result is {result}')
    exit(0)
