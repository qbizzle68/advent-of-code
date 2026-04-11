import sys
import re


def import_data(path: str) -> dict:
    with open(path) as f:
        data = f.read().splitlines()

    rtn = []
    for d in data:
        line_data = {}

        chars = ''.join(re.findall(r'([a-z]+)-', d))
        unique_chars = set(chars)
        char_counts = sorted(((chars.count(c), c) for c in unique_chars), reverse=True)
        line_data['chars'] = char_counts
        
        match = re.search(r'(\d+)\[([a-z]{5})\]', d)
        if match is None:
            raise ValueError(f"error parsing line: '{d}'")
        line_data['id'] = int(match.group(1))
        line_data['checksum'] = match.group(2)

        rtn.append(line_data)
    
    return rtn


def find_most_occurrences(counts: list[int, str]) -> str:
    """Find the 5 most common character counts, using
    alphabetic order on ties. The list is returned as a
    single string. `counts` must already be sorted.
    """

    target_length = counts[4][0]
    passing_counts = [c for c in counts if c[0] >= target_length]
    if len(passing_counts) == 5:
        return ''.join([c[1] for c in passing_counts])
    
    tied_count_value = passing_counts[-1][0]
    tied_counts = [c for c in counts if c[0] == tied_count_value]
    ordered_tied_counts = sorted(tied_counts, key=lambda o: o[1])

    non_tied_counts = [c for c in passing_counts if c[0] > tied_count_value]
    non_tied_counts_count = len(non_tied_counts)

    return ''.join(map(lambda o: o[1], non_tied_counts + ordered_tied_counts[:(5 - non_tied_counts_count)]))


def main(data: dict) -> int:
    accumulator = 0

    for d in data:
        top_chars = find_most_occurrences(d['chars'])
        for c in d['checksum']:
            if c not in top_chars:
                break
        else:
            accumulator += d['id']

    return accumulator


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Syntax: {sys.argv[0]} INPUTPATH')
    input_path = sys.argv[1]

    data = import_data(input_path)
    
    result = main(data)
    print(f'Result is {result}')
