import re
import sys
from enum import Enum


class Instruction(Enum):
    TURN_ON = 0
    TURN_OFF = 1
    TOGGLE = 2


def import_data(path: str) -> list[str]:
    with open(path) as f:
        data = f.readlines()

    return data


def create_instructions(data: list[str]) -> tuple[Instruction, tuple[int, int], tuple[int, int]]:
    instructions = []
    pattern="^(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)$"
    prog = re.compile(pattern)
    for d in data:
        result = prog.match(d)
        if result is None:
            raise Exception(f"Unable to match {d}")

        inst_match = result.group(1)
        instruction = getattr(Instruction, inst_match.replace(' ', '_').upper())
        from_coords = (int(result.group(2)), int(result.group(3)))
        to_coords = (int(result.group(4)), int(result.group(5)))

        instructions.append((instruction, from_coords, to_coords))

    return instructions


def set_lights(lights: list[list[bool]], instructions) -> None:
    for instruction, (x0, y0), (x1, y1) in instructions:
        for i in range(x0, x1+1):
            for j in range(y0, y1+1):
                if instruction is Instruction.TURN_ON:
                    lights[i][j] += 1
                elif instruction is Instruction.TURN_OFF:
                    lights[i][j] = max(0, lights[i][j]-1)
                else:
                    lights[i][j] += 2


def count_lights(lights: list[list[int]]) -> int:
    count = 0
    for i in range(1000):
        for j in range(1000):
            count += lights[i][j]

    return count


def main(path: str) -> int:
    data = import_data(path)
    instructions = create_instructions(data)

    lights = [[0 for _ in range(1000)] for _ in range(1000)]
    set_lights(lights, instructions)

    count = count_lights(lights)
    print(f'Lights have a total brightness of {count}.')

    return 0


if __name__ == '__main__':
    path=sys.argv[1]
    main(path)
