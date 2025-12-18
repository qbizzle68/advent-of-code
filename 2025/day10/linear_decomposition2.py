import sys
import math

import sympy

from part1 import parse_input
from nnary_counter import NnaryCounter
from non_square import solve

def solve_non_singular_matrix(A: sympy.Matrix, b: list[int]) -> list[int]:
    augmented = A.row_join(b)
    rref_matrix = augmented.rref(pivots=False)

    #return [i[0] for i in rref_matrix[:, -1][0]]
    return [i for i in rref_matrix[:, -1]]


def solve_singular_matrix(A: sympy.Matrix, b: list[int]) -> list[int]:
    augmented = A.row_join(b)
    rref = augmented.rref(pivots=False)
    # print(f'{rref=}')
    # exit(0)

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
    #print(f'{len(free_var_indices)} free variables at indices {free_var_indices}')
    # Dim will be number of buttons, found by counting how many columns were padded with zero.
    # This should reduce the number of free variables and speed up computations.
    skip_free_var_count = 0
    for i in range(rref.rows - 1, -1, -1):
        if all(e == 0 for e in rref[:,i]):
            skip_free_var_count += 1
        else:
            break
    # print(f'{rref=}')
    # print(f'{free_var_indices=}')
    # print(f'{skip_free_var_count=}')

    answers_to_copy = [tmp[0] for tmp in rref[:, -1].tolist()]
    x_vals = None
    iterations = 100
    iteration = 0
    invalid_iterations = 100000
    invalid_count = 0
    min_sum = float('inf')
    min_solution = None

    # If there is a negative number in the right hand column of rref, we need the counts to sum to at least that number.
    # In fact, this needs to happen for the "largest" negative number, i.e. largest magnitude. Otherwise, the resulting
    # non-free variable will always be negative and we must strictly have non-negative answers.
    negative_answers = []
    for i, ans in enumerate(answers_to_copy):
        if ans >= 0:
            continue
        # find the largest magnitude of scalar on a free variable
        max_scalar = max((rref.row(i)[x] for x in free_var_indices), key=lambda o: abs(o))
        negative_answers.append(abs(ans // max_scalar))
    # negative_answers = [int(i) for i in answers_to_copy if i < 0]
    if negative_answers:
        start_counts = min(negative_answers)
    else:
        start_counts = 0
    # start_counts = 0
    # print(f'{start_counts=}')
    # print(f'{start_counts=}')
    # The max value is irrelevant here
    #for counts in NnaryCounter(len(free_var_indices), 100000):
    for counts in NnaryCounter(len(free_var_indices) - skip_free_var_count, start_value=start_counts, max_value=100000):
        #print(f'{counts=}')
        if invalid_count >= invalid_iterations:
            if x_vals is not None:
                #print(f'breaking via invalid count')
                break
        elif iteration >= iterations:
            #print(f'breaking from iterations count')
            break
        invalid_state = False
        # I think we can keep this because we'll just keep the last `dim` free variables zero.
        x_vals = [0] * rref.rows
        for val, idx in zip(counts, free_var_indices):
            x_vals[idx] = val
        

        # Iterate from last row to first
        answers = answers_to_copy.copy()
        #for i in range(dim - 1, -1, -1):
        for i in range(rref.rows - 1, -1, -1):
            try:
                first_non_zero = rref.row(i).tolist()[0].index(1)
            except ValueError:
                # Empty row
                continue

            answer = answers[i]
            # Iterate from last column to first non-zero column, then answers[j] will
            # have x_j
            #for j in range(rref.rows - free_var_count - 1, first_non_zero, -1):
            for j in range(rref.rows - 1 - skip_free_var_count, first_non_zero, -1):
            #for j in range(rref.rows - 1, first_non_zero, -1):
                answer -= x_vals[j] * rref.row(i)[j]
                #if answer < 0:
                 #   invalid_state = True
                  #  break
            #if invalid_state is True:
            if answer < 0:
                invalid_state = True
                break
            else:
                x_vals[first_non_zero] = answer

        if invalid_state:
            invalid_count += 1
            if invalid_count % 10000 == 0:
                print(f'{invalid_count=}')
                print(f'{x_vals=}')
            continue
        # Only count iterations where we found a valid number
#        iteration += 1
        
        if A @ sympy.Matrix(x_vals) != b:
            print(f'invalid solution')
            print(f'{x_vals=}')
            print(f'{counts=}')
            exit(1)

        if not all(v.is_integer for v in x_vals):
            continue

        x_vals_sum = sum(x_vals)
        if x_vals_sum < min_sum:
            min_sum = x_vals_sum
            min_solution = x_vals.copy()
            # We want to keep searching until we have `iterations` non-min solutions, so
            # reset when we find a minimum solution
            # iteration = 0
            # invalid_count = 0
            invalid_count -= 100
            # invalid_iterations = 100
        # else:
        iteration += 1
        
    if min_solution is None:
        raise Exception(f'Didn\'t find a valid solution within {iterations} iterations')

    return min_solution


def create_matrices(machine) -> tuple[sympy.Matrix, sympy.Matrix]:
    dim = max(len(machine['buttons']), len(machine['joltage']))
    A = [[1 if i in d else 0 for d in machine['buttons']] for i in range(dim)]
    b = list(machine['joltage'] + (0,) * (dim - len(machine['joltage'])))

    # dim = max(len(machine['buttons']), len(machine['joltage']))
    # tmp = sympy.Matrix([[1 if i in d else 0 for d in machine['buttons']] for i in range(dim)])
    # A = sympy.zeros(dim, dim)
    # A[:tmp.shape[0], :tmp.shape[1]] = tmp
    # b = sympy.Matrix(machine['joltage'] + (0,) * (dim - len(machine['joltage'])))

    return A, b


def main(data) -> int:
    total_sum = 0
    for n, machine in enumerate(data):
    # for machine in [data[144]]:
        # print(machine)
        # dim = max(len(machine['buttons']), len(machine['joltage']))
        # tmp = sympy.Matrix([[1 if i in d else 0 for d in machine['buttons']] for i in range(dim)])
        # A = sympy.zeros(dim, dim)
        # A[:tmp.shape[0], :tmp.shape[1]] = tmp
        # b = sympy.Matrix(machine['joltage'] + (0,) * (dim - len(machine['joltage'])))
        A, b = create_matrices(machine)

        # if A.det() == 0:
        #     # result = solve_singular_matrix(A, b)
        #     result = solve(A, b)
        # else:
        #     result = solve_non_singular_matrix(A, b)
        result = solve(A, b)

        total_sum += int(sum(result))
        # print(f'{n}/{len(data)} completed ...')

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
