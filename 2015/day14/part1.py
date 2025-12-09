import sys
import re


def parse_input(filepath: str) -> dict[str, dict[str, int]]:
    regex = re.compile('^([a-zA-Z]+) can fly ([0-9]+) km/s for ([0-9]+) seconds, but then must rest for ([0-9]+) seconds.$')
    with open(filepath) as f:
        data = f.readlines()

    reindeer_data = {}
    for d in data:
        match = regex.match(d)
        if match is None:
            raise Exception('Unable to parse {d}')

        reindeer_data[match.group(1)] = {'speed': int(match.group(2)),
                                         'fly': int(match.group(3)),
                                         'rest': int(match.group(4))}
    
    return reindeer_data


def main(data: dict[str, dict[str, int]], time: int) -> int:
    distances = [0] * len(data)
    for i, d in enumerate(data):
        cycle_period = data[d]['fly'] + data[d]['rest']
        number_of_cycles = time / cycle_period
        base_distance = int(number_of_cycles) * data[d]['speed'] * data[d]['fly']
        remaining_time = (number_of_cycles % 1.0) * cycle_period
        additional_flight_time = min((remaining_time, data[d]['fly']))
        distances[i] = round(base_distance + additional_flight_time * data[d]['speed'])

    return max(distances)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'Usage: {sys.argv[0]} FILEPATH SECONDS')
        exit(1)
    filepath = sys.argv[1]
    time = int(sys.argv[2])

    data = parse_input(filepath)
    result = main(data, time)
    print(f'Winning reindeer traveled {result} km.')
    exit(0)
