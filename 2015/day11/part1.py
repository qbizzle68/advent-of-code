import sys
import re


def convert_string_to_data(password: str) -> list[int]:
    return [int(b) for b in bytes(password, 'utf-8')]


def increment_password(password: list[int]) -> list[int]:
    result = [v for v in password]
    pointer = len(result) - 1
    while pointer >= 0:
        result[pointer] += 1

        # check for roll-over
        if result[pointer] > 0x7a: # 'z'
            result[pointer] = 0x61 # 'a'
            pointer -= 1
            continue
        else:
            if result[pointer] in (0x69, 0x6c, 0x6F): # (i, l, i)
                result[pointer] += 1
                # Don't need to re-check for roll-over because the
                # value won't go over z
        break
    return result


def is_valid_password(password: list[int]) -> bool:
    # Check incresing straight of at least three letter
    has_straight = False
    for i in range(len(password) - 2):
        if (password[i] + 1 == password[i+1]
            and password[i] + 2 == password[i+2]):
            has_straight = True
            break

    if has_straight is False:
        return False

    # Check for only double repeating letters
    regex = re.compile(r'([a-z])\1{1,}')
    start = 0
    double_count = 0
    str_password = bytes(password).decode()
    while True:
        match = regex.search(str_password[start:])
        if match is None:
            break

        span = match.span()
        double_count += 1
        # We need to ADD this to the existing value since the span values
        # are relative to start (since that's the 0-index of the string we passed)
        start += span[1]
        if start >= len(str_password):
            break
        
    if double_count < 2:
        return False
    
    # The addition portion should not ever reach an invalid letter, but
    # as a stand alone function we shouldn't assume that so check those
    # values aren't in the string
    for c in str_password:
        if c in ('i', 'l', 'o'):
            return False

    return True


def main(current_password: str) -> str:
    password = convert_string_to_data(current_password)
    # Need to increment at least once to find the new one
    password = increment_password(password)
    while not is_valid_password(password):
        password = increment_password(password)

    return bytes(password).decode()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} PASSWORD')
    current_password = sys.argv[1]

    new_password = main(current_password)
    print(f'Next valid password is {new_password}')
    exit(0)
