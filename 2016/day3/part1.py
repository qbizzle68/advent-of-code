import sys


def input_data(path: str) -> list[list[int]]:
    with open(path) as f:
        data = f.read().splitlines()
    
    return [list(map(lambda o: int(o), d.split())) for d in data]


def main(data: list[list[int]]) -> int:
    count = 0

    for d in data:
        # Must explicitly remove only 1 side in case of 2 sides being equal and longest
        longest_side = max(d)
        longest_idx = d.index(longest_side)
        other_sides = d[:]
        other_sides.pop(longest_idx)

        if other_sides[0] + other_sides[1] > longest_side:
            count += 1

    return count


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Syntax: {sys.argv[0]} INPUTPATH')
    input_path = sys.argv[1]

    data = input_data(input_path)

    result = main(data)
    print(f'{result} possible triangles')
