import sys
import re
from collections import defaultdict


def parse_input(data: list[str]) -> list[dict[str, int]]:
    sue_data = []
    regex = re.compile('([a-z]+): ([0-9]+)')
    for line in data:
        match = regex.findall(line)
        if match == []:
            raise Exception(f'Unable to parse {line}')

        d = defaultdict(int)
        for k, v in match:
            d[k] = int(v)
        sue_data.append(d)

    return sue_data


def main(sue_data: list[dict[str, int]], output_data: dict[str, int]) -> int:
    matches = {}
    for i, sue in enumerate(sue_data):
        is_match = True
        for k, v in sue.items():
            if output_data[k] != v:
                is_match = False
                break
        if is_match:
            matches[i] = sue

    return matches


if __name__ == '__main__':
    # no args, just hard-coding filenames since there's no example here

    output_data = {
            'children': 3,
            'cats': 7,
            'samoyeds': 2,
            'pomeranians': 3,
            'akitas': 0,
            'vizslas': 0,
            'goldfish': 5,
            'trees': 3,
            'cars': 2,
            'perfumes': 1,
    }

    with open('input.txt') as f:
        input_data = f.readlines()

    sue_data = parse_input(input_data)
    result = main(sue_data, output_data)
    if len(list(result.keys())) != 1:
        print(f'Unable to find unique answer (len(result) result(s) found).')

    answer = int(next(iter(result))) + 1
    print(f'Aunt Sue {answer} sent the gift!')
