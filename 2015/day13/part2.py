import sys
import re
import itertools
from collections import defaultdict


def parse_input(filepath: str) -> dict[str, dict[str, int]]: 
    with open(filepath) as f:
        file_data = f.readlines()

    identifier = '[a-zA-Z]+'
    regex = re.compile(f'^({identifier}) would (gain|lose) ([0-9]+) happiness units by sitting next to ({identifier}).$')

    happiness_data = defaultdict(dict)
    for d in file_data:
        match = regex.match(d)
        if match is None:
            raise Exception(f'Unable to parse field {d}')

        value = int(match.group(3))
        if match.group(2) == 'lose':
            value *= -1
        happiness_data[match.group(1)][match.group(4)] = value

    # Add 'me' to each persons dict with a value of 0
    for name in happiness_data:
        happiness_data[name]['me'] = 0
    # Add 'me' to overall dict with each person's value equal to 0
    happiness_data['me'] = dict.fromkeys(happiness_data, 0)

    return happiness_data


def main(data: dict[str, dict[str, int]]) -> int:
    max_happiness = 0
    max_happiness_order = None
    for arrangement in itertools.permutations(data.keys()):
        happiness = 0
        for (person1, person2) in itertools.pairwise(arrangement):
            # fixme: this can be more efficient if these values are just combined
            # in parsing the original input
            happiness += (data[person1][person2] + data[person2][person1])
        # Need to add the happiness of the first and last person as well
        happiness += (data[arrangement[0]][arrangement[-1]] + data[arrangement[-1]][arrangement[0]])

        if happiness > max_happiness:
            max_happiness = happiness
            max_happiness_order = arrangement
    print(max_happiness_order)
    return max_happiness 


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} FILEPATH')
    filepath = sys.argv[1]

    data = parse_input(filepath)
    happiness_change = main(data)
    print(f'Optimal happiness change is {happiness_change}.')
