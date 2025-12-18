import sys

import numpy as np

from part1 import parse_input


def is_singular_matrix(buttons: list[tuple[int, ...]]) -> bool: #, joltage: tuple(int)) -> bool:
    A = np.array([[1 if i in d else 0 for d in buttons] for i in range(len(buttons))])
#    b = np.array([joltage[i] if i < len(joltage) else 0 for i in range(len(buttons))])

    return np.linalg.det(A) == 0


def main(data) -> tuple[int, list]:
    # Returns the number of invertible matricies from the data buttons
    accumulator = 0
    singular_matricies = []
    for d in data:
        is_singular = is_singular_matrix(d['buttons'])
        if is_singular:
            accumulator += 1
            singular_matricies.append(d['buttons'])

    return accumulator, singular_matricies

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} FILEPATH')
    filepath = sys.argv[1]

    data = parse_input(filepath)
    singular_count, singular_matrices = main(data)

    print(f'Found {singular_count} singular matrices out of {len(data)}')
    print(f'First singular matrix is {singular_matrices[0]}')
    exit(0)
