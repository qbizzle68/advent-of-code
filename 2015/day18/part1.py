import sys
from collections import defaultdict


def parse_input(filepath: str) -> defaultdict[tuple[int, int], int]:
    map_ = defaultdict(int)
    with open(filepath) as f:
        data = f.readlines()

    rows = len(data)
    # Subtract 1 for the '\n' char
    cols = len(data[0]) - 1
    for i in range(rows):
        for j in range(cols):
            map_[(i, j)] = int(data[i][j] == '#')

    return map_, rows, cols


def _count_neighbors():
    count_memos = {}

    def wrapper(state: defaultdict[tuple[int, int], int], i: int, j: int):
        neighbor_values = (
                state[(i - 1, j - 1)],
                state[(i - 1, j)],
                state[(i - 1, j + 1)],
                state[(i, j - 1)],
                state[(i, j + 1)],
                state[(i + 1, j - 1)],
                state[(i + 1, j)],
                state[(i + 1, j + 1)]
        )
                
        tmp = count_memos.get(neighbor_values)
        if tmp is not None:
            return tmp
        else:
            value = sum(neighbor_values)
            count_memos[neighbor_values] = value
            return value

    return wrapper


count_neighbors = _count_neighbors()


def main(state: defaultdict[tuple[int, int], int], rows: int,
         cols: int, iterations: int) -> int:

    for _ in range(iterations):
        new_state = defaultdict(int)

        for i in range(rows):
            for j in range(cols):
                neighbor_count = count_neighbors(state, i, j)
                key = (i, j)
                if state[key] == 1 and neighbor_count not in (2, 3):
                    new_state[key] = 0
                elif state[key] == 0 and neighbor_count == 3:
                    new_state[key] = 1
                        
        state.update(new_state)

    return sum(state.values())


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'Usage: {sys.argv[0]} FILEPATH ITERATIONS')
    filepath = sys.argv[1]
    iterations = int(sys.argv[2])

    state, rows, cols = parse_input(filepath)
    result = main(state, rows, cols, iterations)
    print(f'Result is {result}')
