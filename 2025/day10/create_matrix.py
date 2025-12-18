import sys

import sympy

from part1 import parse_input


def main(data):
    for machine in data:
        dim = max(len(machine['buttons']), len(machine['joltage']))
        tmp = sympy.Matrix([[1 if i in d else 0 for d in machine['buttons']] for i in range(dim)])
        b = sympy.Matrix(machine['joltage'] + (0,) * (dim - len(machine['joltage'])))
        A = sympy.zeros(dim, dim)
        A[:tmp.shape[0], :tmp.shape[1]] = tmp

        print(f'{A=}')
        print(f'{b=}')


if __name__ == '__main__':
    data = parse_input('example-input.txt')
    main(data)
