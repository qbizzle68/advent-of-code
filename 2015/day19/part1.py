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
    replaced_molecules = set()
    for k, v in maps.items():
        pointer = 0
        while pointer < len(molecule):
            start = molecule.find(k, pointer)
            if start == -1:
                break

            for replace_str in v:
                end = start + len(k)
                new_molecule = molecule[0:start] + replace_str + molecule[end:]
                replaced_molecules.add(new_molecule)

            pointer = start + 1

    return len(replaced_molecules)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} FILEPATH')
    filepath = sys.argv[1]

    maps, molecule = parse_input(filepath)
    result = main(maps, molecule)
    print(f'Result is {result}')
