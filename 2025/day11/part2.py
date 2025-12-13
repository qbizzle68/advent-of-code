import sys
import re


def parse_input(filepath: str) -> dict[str, list[str]]:
    with open(filepath) as f:
        data = f.readlines()

    connections = {}
    for d in data:
        match = re.findall('[a-zA-Z]{3}', d)
        if match == []:
            raise Exception(f'Unable to parse line {d}')
        
        connections[match[0]] = match[1:]
    connections['out'] = []

    return connections


def main(data: dict[str, list[str]], start_node: str) -> int:
    cache = {}

    def count_paths(node: str, has_seen_fft: bool = False, has_seen_dac: bool = False):
        calling_key = (node, has_seen_fft, has_seen_dac)
        if (val := cache.get(calling_key)) is not None:
            return val

        if node == 'out':
            return 1 * (has_seen_fft and has_seen_dac)
        elif node == 'dac':
            has_seen_dac = True
        elif node == 'fft':
            has_seen_fft = True

        result = sum(count_paths(link, has_seen_fft, has_seen_dac) for link in data[node])
        cache[calling_key] = result
        return result
    
    return count_paths(start_node)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} FILEPATH')
    filepath = sys.argv[1]

    data = parse_input(filepath)
    result = main(data, 'svr')

    print(f'Result = {result}')
    exit(0)
