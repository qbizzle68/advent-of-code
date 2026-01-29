import sys
import re


def parse_input(filepath: str) -> tuple[dict[str, list[str]], str]:
    with open(filepath) as f:
        data = f.readlines()

    molecule = data[-1].rstrip()

    # Last 2 lines should be '\n' then molecule
    maps: dict[str, list[str]] = {}
    regex = re.compile('([a-zA-Z]+) => ([a-zA-Z]+)')
    for line in data[:-2]:
        match = regex.match(line.rstrip())
        if match is None:
            raise Exception(f'couldn\'t match line {line}')

        k, v = match.group(1), match.group(2)
        if k not in maps:
            maps[k] = [v]
        else:
            maps[k].append(v)

    return maps, molecule


def main(maps: dict[str, list[str]], molecule: str) -> int:
    finished_molecules = []

    def backtrack(current_string: str, pointer: int, additions: int):
        if current_string == molecule:
            finished_molecules.append((current_string, additions))
            return
        if pointer >= len(current_string) or len(current_string) >= len(molecule):
            print('breaking')
            print(f'{pointer=}')
            print(f'{current_string}')
            return

        # We need to check if the part of the string pointed at by pointer can be replaced.
        # If the value is just a capital letter it's the value to check, otherwise include a
        # following lowercase letter.
        # Make sure we're not at the end of the string
        if pointer + 1 < len(current_string) and current_string[pointer + 1].islower():
            backtrack(current_string, pointer + 2, additions)
            candidate = current_string[pointer:pointer + 2]
            size = 2
        else:
            # Not sure if we need to possible try not replacing at the current spot.
            # If so, right here is where we would recurse on backtrack with pointer + 1
            backtrack(current_string, pointer + 1, additions)
            candidate = current_string[pointer]
            size = 1

        valid_mappings = {k: v for k, v in maps.items() if k == candidate}
        if len(valid_mappings) == 0:
            new_pointer = pointer + 1
            if new_pointer < len(current_string) and current_string[pointer + 1].islower():
                new_pointer += 1
            backtrack(current_string, new_pointer, additions)
        else:
            for k, v in valid_mappings.items():
                for vv in v:
                    new_string = current_string[:pointer] + vv + current_string[pointer + size:]
                    backtrack(new_string, pointer + size, additions + 1)

    for k, v in maps.items():
        if k == 'e':
            for vv in v:
                backtrack(vv, 0, 1)

    # Don't know if we need the string?
    return min(finished_molecules, key=lambda o: o[1])
    

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} FILEPATH')
    filepath = sys.argv[1]

    maps, molecule = parse_input(filepath)
    result = main(maps, molecule)
    print(f'Result is {result}')
