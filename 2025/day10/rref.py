import sys
from sympy import Matrix


if __name__ == '__main__':
 #   if len(sys.argv) != 1:
#        print(f'Usage: {sys.argv[0]}')

    A = Matrix([[0, 0, 0, 0, 1, 1],
                [0, 1, 0, 0, 0, 1],
                [0, 0, 1, 1, 1, 0],
                [1, 1, 0, 1, 0, 0]])
    b = Matrix([3, 5, 4, 7])

    augmented = A.row_join(b)
    print(augmented)

    rref_matrix, pivot = augmented.rref()
    print(rref_matrix)
