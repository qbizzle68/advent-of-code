import sys


class Row:
    def __init__(self, string: str) -> None:
        self.str = string
        self.splitters = [i for i, c in enumerate(string) if c == '^']
        self.splits = 0
    
    def add_beam(self, idx: int) -> None:
        if self.str[idx] == '^':
            self.str = self.str[:idx-1] + '|^|' + self.str[idx+2:]
            self.splits += 1
        else:
            self.str = self.str[:idx] + '|' + self.str[idx+1:]

    def __str__(self) -> str:
        return self.str

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.str})'


class Diagram:
    def __init__(self, diagram: str) -> None:
        strings = diagram.splitlines()
        self.rows = [Row(s) for s in strings]

    def __str__(self) -> str:
        return '\n'.join(map(str, self.rows))

    def activate_beam(self) -> None:
        # Want to raise if 'S' can't be found
        beam_start = self.rows[0].str.index('S')
        beam_indexes = [beam_start]
        for row in self.rows[1:]:
            for idx in beam_indexes:
                row.add_beam(idx)

            beam_indexes = (i for i, c in enumerate(row.str) if c == '|')




def main(filepath: str) -> int:
    with open(filepath) as f:
        data = f.read()

    diagram = Diagram(data)
#    print(f'diagram is \n{diagram}')
    diagram.activate_beam()
 #   print(f'diagram with beams is\n{diagram}')

    splits = sum(r.splits for r in diagram.rows)
    return splits


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} FILEPATH')
    filepath = sys.argv[1]

    splits = main(filepath)
    print(f'Number of splits is {splits}')
    exit(0)
