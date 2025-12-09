import sys
import itertools


def main(data: list[int], size) -> int:
    count = 0
    for i in range(len(data), 1, -1):
        for f in itertools.combinations(data, len(data) - i):
            if sum(f) == size:
                count += 1

    return count


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'Usage: {sys.argv[0]} FILEPATH SIZE')
    filepath = sys.argv[1]
    size = int(sys.argv[2])

    with open(filepath) as f:
        raw_data = f.readlines()

    data = tuple(map(int, raw_data))
    result = main(data, size)
    print(f'Result is {result}')
