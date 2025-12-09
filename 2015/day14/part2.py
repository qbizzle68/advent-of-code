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
    reindeer_count = len(data)
    points = [0] * reindeer_count
    distances = [0] * reindeer_count
    states = ['fly'] * reindeer_count
    time_in_state = [0] * reindeer_count

    for t in range(time):
        for i, d in enumerate(data): #range(reindeer_count):
            if states[i] == 'fly':
                if time_in_state[i] == data[d]['fly']:
                    states[i] = 'rest'
                    # This iteration counts as the first second in the state (not 0th)yy
                    time_in_state[i] = 1
                else:
                    distances[i] += data[d]['speed']
                    time_in_state[i] += 1
            else:
                if time_in_state[i] == data[d]['rest']:
                    states[i] = 'fly'
                    distances[i] += data[d]['speed']
                    # This iteration counts as the first second in the state (not 0th)yy
                    time_in_state[i] = 1
                else:
                    time_in_state[i] += 1

        lead_distance = max(distances)
        lead_reindeers = (i for i, d in enumerate(distances) if d == lead_distance)
        for reindeer in lead_reindeers:
            points[reindeer] += 1

    return max(points)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'Usage: {sys.argv[0]} FILEPATH SECONDS')
        exit(1)
    filepath = sys.argv[1]
    time = int(sys.argv[2])

    data = parse_input(filepath)
    result = main(data, time)
    print(f'The most points are {result}.')
    exit(0)
