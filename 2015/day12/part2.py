import sys
import json


def count_numbers(data: dict | list | int) -> int:
    # Base cases
    if isinstance(data, int):
        return data
    if data == [] or data == {}:
        return 0

    if isinstance(data, list):
        itr = iter(data)
    elif isinstance(data, dict):
        if any("red" == v for v in data.values()):
            return 0
        itr = iter(data.values())
    else:
        # I think the only other data type to worry about is a str, but either
        # way we should just skip anything that cannot contain a nested structure
        # instead of raising an exception
        return 0
        #raise Exception(f'data is of type {type(data)}')

    sum = 0
    for val in itr:
        sum += count_numbers(val)

    return sum


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} JSONPATH')
    filepath = sys.argv[1]

    with open(filepath) as f:
        data = json.load(f)

    number_sum = count_numbers(data)
    print(f'Total sum of numbers found is {number_sum}')
