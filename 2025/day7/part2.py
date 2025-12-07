import sys
from collections import defaultdict


"""I really love this solution. I tried some OOP design that mapped
a single beam and spawned a new literal object when it split but
it was extremely inefficient. Cool idea, no idea how much time it
actually would have taken to finish but this solution is not only
simpler but only iterates on the diagram text a single time to find
the solution. O(n) where n is bytes in the diagram text."""


def main(filepath: str) -> int:
    with open(filepath) as f:
        data = f.read()

    diagram = data.rstrip().splitlines()
    start_column = diagram[0].index('S')
    beam_positions = defaultdict(int)
    beam_positions[(1, start_column)] = 1
    
    number_of_columns = len(diagram[0])        
    for i in range(1, len(diagram) - 1):
        for j in range(number_of_columns):
            if beam_positions[(i, j)] > 0:
                count = beam_positions[(i, j)]
                if diagram[i+1][j] == '^':
                    beam_positions[(i, j)] = 0
                    beam_positions[(i+1, j-1)] += count
                    beam_positions[(i+1, j+1)] += count
                else:
                    beam_positions[(i, j)] = 0
                    beam_positions[(i+1, j)] += count

    return sum(beam_positions.values())


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} FILEPATH')
    filepath = sys.argv[1]

    timelines = main(filepath)
    print(f'Number of timelines is {timelines}')
    exit(0)
