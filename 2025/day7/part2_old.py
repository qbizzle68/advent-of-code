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

    def __getitem__(self, idx: int) -> str:
        return self.str[idx]


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

    def __getitem__(self, idx: int) -> 'Row':
        return self.rows[idx]


class LaserBeam:
    def __init__(self, position: list[int, int] | None = None) -> None:
        self.position = position if position is not None else [0, 0]

    def make_copy(self) -> 'LaserBeam':
        tmp = object.__new__(self.__class__)
        tmp.position = [v for v in self.position]
        return tmp

    def set_position(self, pos: list[int, int]) -> None:
        self.position = pos


def main(filepath: str) -> int:
    with open(filepath) as f:
        data = f.read()

    diagram = Diagram(data)
    start_column = diagram.rows[0].str.index('S')
    laser_beams = [LaserBeam([1, start_column])]
    last_row_index = len(diagram.rows) - 1

    stop = False
    while not stop:
        stop = True

        for beam in [b for b in laser_beams if b.position[0] < last_row_index]:
            pos = beam.position
            if diagram[pos[0] + 1][pos[1]] == '^':
                beam.position = [pos[0] + 1, pos[1] - 1]
                new_beam = beam.make_copy()
                new_beam.position = [pos[0] + 1, pos[1] + 1]
                laser_beams.append(new_beam)
            else:
                beam.position = [pos[0] + 1, pos[1]]
            stop = False

    return len(laser_beams)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} FILEPATH')
    filepath = sys.argv[1]

    timelines = main(filepath)
    print(f'Number of timelines is {timelines}')
    exit(0)
