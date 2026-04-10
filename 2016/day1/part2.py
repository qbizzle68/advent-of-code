import sys


def import_file(path: str) -> list[tuple[str, int]]:
    with open(path) as f:
        data = f.read().split(', ')

    return [(d[0], int(d[1:])) for d in data]


def move(data: list[tuple[str, int]]) -> tuple[int, int]:
    moves = [0] * 4     # total moves in direction [north, east, south, west]
    direction_index = 0
    positions = set()

    for turn, count in data:
        if turn == 'R': direction_index = (direction_index + 1) % 4
        elif turn == 'L': direction_index = (direction_index - 1) % 4
        else:
            raise ValueError(f'turn direction must be L or R, not {turn}')

        for _ in range(1, count + 1):
            moves[direction_index] += 1

            position = (moves[0] - moves[2], moves[1] - moves[3])
            if position in positions:
                return position
            else:
                positions.add(position)

    raise RuntimeError(f"Didn't visit a location more than once")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Syntax: {sys.argv[0]} INPUTPATH")
        exit(1)
    
    input_path = sys.argv[1]

    data = import_file(input_path)
    answer = move(data)

    print(f"Second visited position: {answer}")
    print(f"Answer: {abs(answer[0]) + abs(answer[1])}")
