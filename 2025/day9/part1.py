import sys
import itertools


def main(data: list[tuple[int, int]]) -> int:
    max_area = 0
    for tile1, tile2 in itertools.combinations(data, 2):
        # Each side length is the inclusive difference, i.e. need to add 1
        area = (abs(tile1[0] - tile2[0]) + 1) * (abs(tile1[1] - tile2[1]) + 1)
        if area > max_area:
            max_area = area

    return max_area


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} FILEPATH')

    filepath = sys.argv[1]
    with open(filepath) as f:
        raw_data = f.readlines()
    
    data = [tuple(map(int, d.rstrip().split(','))) for d in raw_data]
    result = main(data)
    print(f'Result is {result}')
