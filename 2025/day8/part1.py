import sys
import itertools
import math
import operator
import heapq


def parse_input(filepath:str) -> list[tuple[int, int, int]]:
    with open(filepath) as f:
        data = f.readlines()

    return list(tuple(map(int, d.rstrip().split(','))) for d in data)


def main(boxes: list[tuple[int, int, int]], iterations: int) -> int:
    connections = dict.fromkeys(boxes, 0)
    idx = 1
    # Compute all minimums and sort them first
    distances = {(b1, b2): math.dist(b1, b2) for b1, b2 in itertools.combinations(boxes, 2)}
    sorted_distances = sorted(distances.items(), key=lambda o: o[1])
    distances = dict(sorted_distances)

    distance_iterator = iter(distances)
    for _ in range(iterations):
        box1, box2 = next(distance_iterator)

        box1_idx = connections[box1]
        box2_idx = connections[box2]
        # New connection
        if box1_idx == box2_idx == 0:
            connections[box1] = idx
            connections[box2] = idx
            idx += 1
            continue

        # Every key in connections whose value is the same as box1 or box2
        # needs to be set to the same. If box1 or box2 is zero then use the
        # other, if both are non-zero either works, we'll use box1
        needs_changing = [i for i in (box1_idx, box2_idx) if i > 0]
        assert len(needs_changing) > 0, 'something went wrong'
        same_idx = box2_idx if box1_idx == 0 else box1_idx
        for k, v in connections.items():
            if v in needs_changing:
                connections[k] = same_idx
        # Don't forget to set box1 and box2
        connections[box1] = same_idx
        connections[box2] = same_idx

    max_val = max(connections.values())
    buffer = [0] * (max_val + 1)
    for val in connections.values():
        if val != 0:
            buffer[val] += 1

    return math.prod(heapq.nlargest(3, buffer))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'Usage: {sys.argv[0]} FILEPATH ITERATIONS')
    filepath = sys.argv[1]
    iterations = int(sys.argv[2])

    input_data = parse_input(filepath)
    answer = main(input_data, iterations)
    print(f'Product of three largest circuits is {answer}')
    exit(0)

