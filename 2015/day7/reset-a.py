import sys
import re
from pprint import pp


"""I really really really wanted to get this to work using a stack, where we
would push instructions we couldn't compute and lookup the instruction that
sets the uncomputed value; repeat. Spent days and couldn't get it to work.
Instead we hand sort the instructions so they're in order and execute them
one by one."""


class InstructionStack:
    def __init__(self):
        self.stack = []

    def push(self, instruction: 'Instruction') -> None:
        self.stack.append(instruction)

    def pop(self) -> 'Instruction | None':
        if len(self.stack) == 0:
            return None
        value = self.stack.pop()
        return value

    def peek(self) -> 'Instruction | None':
        return None if len(self.stack) == 0 else self.stack[-1]
    
    def __contains__(self, val) -> bool:
        for instruction in self.stack:
            if instruction.sets == val:
                return True

        return False

    def __len__(self) -> int:
        return len(self.stack)


class Instruction:
    def __init__(self, command: str, sets: str, variables: tuple[str], value: int | None = None) -> None:
        self.command = command
        self.sets = sets
        self.variables = variables
        self.value = value

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.command}, {self.sets}, {self.variables}, {self.value})'

    def __eq__(self, other: 'Instruction') -> bool:
        return self is other

    def __lt__(self, other: 'Instruction') -> bool:
        # Less than is if this instruction must be executed before other
        return self.sets in other.variables[:-1]

    def __gt__(self, other: 'Instruction') -> bool:
        return other.sets in self.variables[:-1]


def parse_input(data: str) -> dict[Instruction]:
    value = '[0-9]+'
    identifier = '[a-z]+'
    set_pattern = f'({value}|{identifier}) -> ({identifier})'
#    setvar_pattern = f'({identifier}) -> ({identifier})'
    binary_pattern = f'(1|{identifier}) (AND|OR) ({identifier}) -> ({identifier})'
    shift_pattern = f'({identifier}) ([LR]SHIFT) ({value}) -> ({identifier})'
    not_pattern = f'NOT ({identifier}) -> ({identifier})'

    lines = data.rstrip().split('\n')
    instructions = {}
    for line in lines:
        if match := re.match(set_pattern, line):
            val = int(match.group(1)) if match.group(1).isnumeric() else None
            instruction = Instruction('SET', match.group(2), (match.group(1), match.group(2)), val)
        elif match := re.match(binary_pattern, line):
            instruction = Instruction(match.group(2), match.group(4), (match.group(1), match.group(3), match.group(4)))
        elif match := re.match(shift_pattern, line):
            instruction = Instruction(match.group(2), match.group(4), (match.group(1), match.group(4)), int(match.group(3)))
        elif match := re.match(not_pattern, line):
            instruction = Instruction('NOT', match.group(2), (match.group(1), match.group(2)))
        else:
            raise Exception(f'Unable to match instruction {line}')

        instructions[match.groups()[-1]] = instruction

    return instructions


def execute_command(instruction: Instruction, wire_values: dict[str, int]):
    if instruction.command == 'SET':
        if instruction.value is None:
            wire_values[instruction.sets] = wire_values[instruction.variables[0]]
        else:
            wire_values[instruction.sets] = instruction.value
    elif instruction.command == 'AND':
        v = instruction.variables
        if v[0].isnumeric():
            lhs = int(v[0])
        else:
            lhs = wire_values[v[0]]
        rhs = wire_values[v[1]]
        wire_values[instruction.sets] = lhs & rhs
    elif instruction.command == 'OR':
        v = instruction.variables
        lhs = wire_values[v[0]]
        rhs = wire_values[v[1]]
        wire_values[instruction.sets] = lhs | rhs
    elif instruction.command == 'LSHIFT':
        lhs = wire_values[instruction.variables[0]]
        wire_values[instruction.sets] = lhs << instruction.value
    elif instruction.command == 'RSHIFT':
        lhs = wire_values[instruction.variables[0]]
        wire_values[instruction.sets] = lhs >> instruction.value
    elif instruction.command == 'NOT':
        v = wire_values[instruction.variables[0]]
        # Force v to be 16 bits
        wire_values[instruction.sets] = ~v & 0xffff
    else:
        raise Exception(f'Invalid command {instruction.command} found')

def main2(instructions: list[Instruction]) -> dict[str, Instruction]:
    pointer = 0
    wire_values = {}
    total_instructions = len(instructions)
    while len(wire_values) < total_instructions:
        print(f'wire value count = {len(wire_values)}')
        working_instruction = instructions[pointer]

        variable_values = (wire_values.get(v) for v in working_instruction.variables[:-1] if not v.isnumeric())
        if all(variable_values):
            execute_command(working_instruction, wire_values)

        pointer = (pointer + 1) % total_instructions

    return wire_values


def sort_main(instructions: list[Instruction]) -> dict[str, Instruction]:
    stop = False
    while not stop:
        stop = True
        for i, to_move in enumerate(instructions):
            move_to_index = None
            for j, compare_to in enumerate(instructions):
                if to_move is compare_to:
                    continue
                # Determine if to_move should be placed at least after compare_to (must already be before)
                if compare_to.sets in to_move.variables[:-1] and i < j:
                    # This is the index AFTER to_move is removed.
                    move_to_index = j
                    # [ 0, 1, 2, 4, 3, 5, 6]
                    # after removing 4  (index = j)
                    # [0, 1, 2, 3, 5, 6]
                    # reinserting at index = j (4)
                    # [0, 1, 2, 3, 4, 5, 6]

            if move_to_index is not None:
                instructions.remove(to_move)
                instructions.insert(move_to_index, to_move)
                stop = False
                break


def process_sorted(instructions: list[Instruction], wire_values: dict[str, int]) -> None:
    for instruction in instructions:
        execute_command(instruction, wire_values)

    
def main(filepath) -> dict[str, int]:
    with open(filepath) as f:
        data = f.read()

    instructions = parse_input(data)
    instructions = list(instructions.values())

    sort_main(instructions)
    wire_values = {}
    process_sorted(instructions, wire_values)

    # Need to take the result of wire a and create a new instruction (overriding) setting
    # b to that value
    new_b = wire_values['a']
    new_b_instruction = Instruction('SET', 'b', ('b',), new_b)
    # search for and replace instruction setting 'b'
    for instruction in instructions:
        if instruction.sets == 'b':
            old_b_instruction = instruction
            break

    idx = instructions.index(old_b_instruction)
    instructions[idx] = new_b_instruction
    new_wire_values = {}
    process_sorted(instructions, new_wire_values)

    return new_wire_values

if __name__ == '__main__':
    filepath = sys.argv[1]
    wire_values = main(filepath)
    
    print('Wire value of a is', wire_values['a'])
