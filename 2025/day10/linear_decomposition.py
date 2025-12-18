import sys

import sympy

from part1 import parse_input
from nnary_counter import NnaryCounter

def solve_non_singular_matrix(A: sympy.Matrix, b: list[int]) -> list[int]:
    augmented = A.row_join(b)
    rref_matrix = augmented.rref(pivots=False)

    return [i[0] for i in rref_matrix[:, -1][0]]


def solve_singular_matrix(A: sympy.Matrix, b: list[int]) -> list[int]:
    augmented = A.row_join(b)
    rref = augmented.rref(pivots=False)

    # Find free variable indices
    free_var_indices = list(range(rref.rows))
    empty_rows = 0
    for i in range(rref.rows):
        for j in range(i, rref.rows):
            if rref.row(i)[j] == 1:
                free_var_indices.remove(j)
                break
            else:
                if j == rref.rows - 1:
                    empty_rows += 1

    # Don't know if this can happen or what staet we'll be in
    assert len(free_var_indices) == empty_rows, 'unmatched empty rows and free variables'
    print(f'{len(free_var_indices)} free variables at indices {free_var_indices}')

    answers_to_copy = [tmp[0] for tmp in rref[:, -1].tolist()]
    x_vals = None
    iterations = 10
    iteration = 0
    invalid_iterations = 1000000
    invalid_count = 0
    min_sum = float('inf')
    min_solution = None
    # The max value is irrelevant here
    for counts in NnaryCounter(len(free_var_indices), 100000):
        if invalid_count >= invalid_iterations:
            if x_vals is not None:
                print(f'breaking via invalid count')
                break
        elif iteration >= iterations:
            print(f'breaking from iterations count')
            break
        invalid_state = False
        x_vals = [0] * rref.rows
        for val, idx in zip(counts, free_var_indices):
            x_vals[idx] = val
        

        # Iterate from last row to first
        answers = answers_to_copy.copy()
        for i in range(rref.rows - 1, -1, -1):
            try:
                first_non_zero = rref.row(i).tolist()[0].index(1)
            except ValueError:
                # Empty row
                continue

            answer = answers[i]
            # Iterate from last column to first non-zero column, then answers[j] will
            # have x_j
            for j in range(rref.rows - 1, first_non_zero, -1):
                answer -= x_vals[j] * rref.row(i)[j]
                if answer < 0:
                    invalid_state = True
                    break
            if invalid_state is True:
                break
            x_vals[first_non_zero] = answer

        if invalid_state:
            invalid_count += 1
            continue
        # Only count iterations where we found a valid number
#        iteration += 1
        
        if A @ sympy.Matrix(x_vals) != b:
            print(f'invalid solution')
            print(f'{x_vals=}')
            print(f'{counts=}')
            exit(1)

        x_vals_sum = sum(x_vals)
        if x_vals_sum < min_sum:
            min_sum = x_vals_sum
            min_solution = x_vals.copy()
            # We want to keep searching until we have `iterations` non-min solutions, so
            # reset when we find a minimum solution
            iteration = 0
            invalid_count = 0
            invalid_iterations = 100
        else:
            iteration += 1

    if min_solution is None:
        raise Exception(f'Didn\'t find a valid solution within {iterations} iterations')

    return min_solution


def main(data) -> int:
    total_sum = 0
    for machine in data:
        dim = max(len(machine['buttons']), len(machine['joltage']))
        #length = len(machine['joltage'])
        tmp = sympy.Matrix([[1 if i in d else 0 for d in machine['buttons']] for i in range(dim)])
        A = sympy.zeros(dim, dim)
        A[:tmp.shape[0], :tmp.shape[1]] = tmp
        print(A)
        b = sympy.Matrix(machine['joltage'] + (0,) * (dim - len(machine['joltage'])))
        print(b)

        if A.det() == 0:
            result = solve_singular_matrix(A, b)
        else:
            result = solve_non_singular_matrix(A, b)

        total_sum += sum(result)

    return total_sum


if __name__ == '__main__':
    '''A = sympy.Matrix([[0, 0, 0, 0, 1, 1],
                      [0, 1, 0, 0, 0, 1],
                      [0, 0, 1, 1, 1, 0],
                      [1, 1, 0, 1, 0, 0],
                      [0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0]])
    b = sympy.Matrix([3, 5, 4, 7, 0, 0])

    print(solve_singular_matrix(A, b))'''

    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} FILEPATH')
        exit(1)
    filepath = sys.argv[1]

    data = parse_input(filepath)
    result = main(data)
    print(f'Result is {result}')
