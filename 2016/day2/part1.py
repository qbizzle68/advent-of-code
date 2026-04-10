import sys


def input_data(path: str) -> list[str]:
    with open(path) as f:
        data = f.read().splitlines()

    return data


def main(data: list[str]) -> int:
    digits = []
    current_key = 5

    for line in data:
        for direction in line:
            if direction == 'U':
                if current_key > 3:
                    current_key -= 3
            elif direction == 'D':
                if current_key < 7:
                    current_key += 3
            elif direction == 'L':
                if current_key not in (1, 4, 7):
                    current_key -= 1
            elif direction == 'R':
                if current_key not in (3, 6, 9):
                 current_key += 1
            else:
                raise ValueError(f'invalid direction, got {direction}')
        digits.append(current_key)

    value = 0
    for digit in digits:
        value = (value * 10 + digit)
    
    return value


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Syntax: {sys.argv[1]} INPUTPATH')
    input_path = sys.argv[1]

    data = input_data(input_path)
    answer = main(data)

    print(f'Code is {answer}')
