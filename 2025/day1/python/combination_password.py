import sys


def import_data(path: str) -> list[int]:
    values = []
    with open(path) as f:
        lines = f.readlines()

    for line in lines:
        values.append(int(line[1:]))
        if line[0] == 'L':
            values[-1] *= -1

    return values


def main(path: str) -> int:
    values = import_data(path)

    dial = 50
    count = 0
    for value in values:
        dial = (dial + value) % 100
        if dial == 0:
            count += 1

    return count        


if __name__ == '__main__':
    path = sys.argv[1]
    password = main(path)
    print("Password is", password)
    exit(0)
