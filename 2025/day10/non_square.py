import sys

import sympy
from pulp import *
# from linear_decomposition2 import create_matrices, parse_input
# from linear_decomposition2 import parse_input


def compress_rref_matrix(rref: sympy.Matrix, free_var_indices: list[int],
                         empty_rows: int, skip_free_var_count: int = 0):
    """Compress a rref matrix by removing all rows and columns
    that for a variable independent of any other free variables.
    """

    row_indices_to_add = []
    for i in range(rref.rows - empty_rows):
        first_index_to_check = rref.row(i).tolist()[0].index(1) + 1
        last_index_to_check = rref.rows - skip_free_var_count
        if any(x != 0 for x in rref.row(i)[first_index_to_check:last_index_to_check]):
            row_indices_to_add.append(i)
    print(f'{row_indices_to_add=}')
    
    # Create empty matrix
    compressed_matrix = [None] * len(row_indices_to_add)
    for i in range(len(row_indices_to_add)):
        compressed_matrix[i] = [0] * (len(row_indices_to_add)
                                     + len(free_var_indices) + 1)

    count = len(row_indices_to_add)
    # Fill compressed matrix
    # Fill diagonals
    for i in range(len(row_indices_to_add)):
        compressed_matrix[i][i] = 1
    # Fill free variables
    for i in range(len(row_indices_to_add)):
        for j, idx in enumerate(free_var_indices):
            compressed_matrix[i][count + j] = rref.row(row_indices_to_add[i])[idx]
    # Fill answers
    for i in range(len(row_indices_to_add)):
        compressed_matrix[i][-1] = rref.row(row_indices_to_add[i])[-1]

    return sympy.Matrix(compressed_matrix)


def solve_singular_matrix(A: sympy.Matrix, b: list[int]) -> list[int]:
    augmented = A.row_join(b)
    rref = augmented.rref(pivots=False)

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

    assert len(free_var_indices) == empty_rows, 'unmatched empty forws and free variable counts'
    
    # Find number of padded columns i.e. columns of all zeros on rhs before rref answers
    skip_free_var_count = 0
    for i in range(rref.rows - 1, -1, -1):
        if all(e == 0 for e in rref[:, i]):
            skip_free_var_count += 1
        else:
            break

    compressed_rref = compress_rref_matrix(rref, free_var_indices,
                                           empty_rows, skip_free_var_count)
    
    print(f'{rref=}')
    print(f'{compressed_rref=}')

    return rref, compressed_rref


def create_matrices(machine) -> tuple[list[list[int]], list[int]]:
    dim = max(len(machine['buttons']), len(machine['joltage']))
    A = [[1 if i in d else 0 for d in machine['buttons']] for i in range(dim)]
    b = list(machine['joltage'] + (0,) * (dim - len(machine['joltage'])))

    # tmp = sympy.Matrix([[1 if i in d else 0 for d in machine['buttons']] for i in range(dim)])
    # A = sympy.zeros(dim, dim)
    # A[:tmp.shape[0], :tmp.shape[1]] = tmp
    # b = sympy.Matrix(machine['joltage'] + (0,) * (dim - len(machine['joltage'])))

    return A, b


def solve(A: list[list[int]], b: list[int]) -> int:
    n = len(A[0])
    m = len(A)

    prob = LpProblem('MinSum', LpMinimize)
    x = [LpVariable(f'x{i}', lowBound=0, cat='Integer') for i in range(n)]

    prob += lpSum(x)
    for i in range(m):
        prob += lpSum([A[i][j] * x[j] for j in range(n)]) == b[i]

    prob.solve(PULP_CBC_CMD(msg=0))

    return [value(x[i]) for i in range(n)]


# if __name__ == '__main__':
#     file = sys.argv[1]
#     idx = int(sys.argv[2])
#     data = parse_input(file)
#     A, b = create_matrices(data[idx])
#     for a in A:
#         print(a)
#     print(b)
#     soln = solve(A, b)
#     print(soln)
    # solve_singular_matrix(A, b)
