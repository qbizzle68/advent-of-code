import sys
import re
import itertools


def import_data(filepath: str) -> dict[tuple[str, str], int]:
    with open(filepath) as f:
        data = f.readlines()
    
    pattern = re.compile('^([a-zA-Z]+) to ([a-zA-Z]+) = ([0-9]+)$')
    distances = {}
    for line in data:
        match = pattern.match(line)
        if not match:
            raise Exception(f'unable to match line {line}')

        distances[(match.group(1),match.group(2))] = int(match.group(3))

    return distances


def main(filepath:str):
    distances = import_data(filepath)
    cities = set(itertools.chain.from_iterable(s[:2] for s in distances))

    path_distances = {}
    for order in itertools.permutations(cities):
        current_distance = 0
        for start, end in itertools.pairwise(order):
            dist = distances.get((start, end))
            if dist is None:
                dist = distances.get((end, start))
            if dist is None:
                raise Exception(f'Unable to get distance between {start} and {end}')

            current_distance += dist

        path_distances[order] = current_distance

    print(f"Minimum distance is {min(path_distances.values())}")


if __name__ == '__main__':
    filepath = sys.argv[1]
    main(filepath)
    exit(0)
