import sys
import re
import itertools
import operator
import math


def parse_input(filepath: str) -> dict[str, dict[str, int]]:
    with open(filepath) as f:
        data = f.readlines()

    ingredients = []
    for line in data:
        match = re.findall('-?[0-9]+', line)
        if len(match) != 5:
            raise Exception(f'Unable to parse data in {line}')

        ingredients.append(tuple(map(int, match)))

    return ingredients


def main(data: dict[str, dict[str, int]], teaspoons: int) -> int:
    combinations = []
    for a in range(teaspoons + 1):
        for b in range(a, teaspoons + 1 - a):
            for c in range(b, teaspoons + 1 - a - b):
                d = 100 - a - b - c
                combinations.extend(set(itertools.permutations((a, b, c, d))))

    ingredient_count = len(data)
    numbers = tuple(range(1, teaspoons + 1))
    scores = []
    for combo in combinations:
        if sum(combo) != 100:
            continue

        capacity_sum = 0
        durability_sum = 0
        flavor_sum = 0
        texture_sum = 0
        for c, ing in zip(combo, data):
            capacity_sum += c * ing[0]
            durability_sum += c * ing[1]
            flavor_sum += c * ing[2]
            texture_sum += c * ing[3]

        score = (max(capacity_sum, 0) * max(durability_sum, 0)
                 * max(flavor_sum, 0) * max(texture_sum, 0))
        scores.append(score)

    return max(scores)
        

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'Usage: {sys.argv[0]} FILEPATH TEASPOONS')
        exit(1)
    filepath = sys.argv[1]
    teaspoons = int(sys.argv[2])

    data = parse_input(filepath)
    result = main(data, teaspoons)
    print(f'Highest score is {result}.')
    exit(0)
