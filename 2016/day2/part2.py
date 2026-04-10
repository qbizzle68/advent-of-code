import sys


def input_data(path: str) -> list[str]:
    with open(path) as f:
        data = f.read().splitlines()

    return data


def main(data: list[str]) -> str:
    digits = []
    current_key = 5

    for line in data:
        for direction in line:
            if direction == 'U':
                if current_key not in (5, 2, 1, 4, 9):
                    current_key -= 4 if current_key not in (3, 13) else 2
            elif direction == 'D':
                if current_key not in (5, 10, 13, 12, 9):
                    current_key += 4 if current_key not in (1, 11) else 2
            elif direction == 'L':
                if current_key not in (1, 2, 5, 10, 13):
                    current_key -= 1
            elif direction == 'R':
                if current_key not in (1, 4, 9, 12, 13):
                 current_key += 1
            else:
                raise ValueError(f'invalid direction, got {direction}')
        digits.append(current_key)

    print(f'{digits}')

    return ''.join(map(lambda o: f'{o:x}', digits))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Syntax: {sys.argv[1]} INPUTPATH')
    input_path = sys.argv[1]

    data = input_data(input_path)
    answer = main(data)

    print(f'Code is {answer}')
