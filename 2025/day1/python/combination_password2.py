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
        dial_was_zero = (dial == 0)
        dial += value
        # This can only be true if value == -dial (therefore abs(value) < 100, so no need to count revolutions)
        if dial == 0:
            count += 1
            continue
        elif dial >= 100:
            q, r = divmod(dial, 100)
            count += q
            dial = r
        elif dial < 0:
            if not dial_was_zero:
                count += 1
            dial *= -1
            q, r = divmod(dial, 100)
            count += q
            dial = r
            
    return count        


if __name__ == '__main__':
    path = sys.argv[1]
    password = main(path)
    print("Password is", password)
    exit(0)
