import sys
import re


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
#        return val in self.stack
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
        return f'{self.__class__.__name__}({self.command}, {self.variables}, {self.value})'


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


def process(instructions: dict[str, Instruction], wire_values: dict[str, int]):
    stack = InstructionStack()
    # We're making the assumption that wire_values all only get set once (I'm pretty sure this is true from
    # the instructions). So when the number of values in wire_values is equal to the number of values that
    # get set in instructions we're done.
    total_instruction_count = len(set(i.sets for i in instructions.values()))
    print(f'total_instruction_count = {total_instruction_count}')
#    while len(instructions) > 0:
    while len(wire_values) < total_instruction_count:
        print(f'length of wire_values = {len(wire_values)}')
        print(f'wire values = {wire_values}')
        next_instruction = stack.peek()
        if next_instruction is None:
            for variable, instruction in instructions.items():
                if wire_values.get(variable) is None:
                    next_instruction = instruction
                    break
#            next_instruction = next(iter(instructions.values()))
            stack.push(next_instruction)
        print(f'next instruction = {next_instruction}')

        # If the operands are None in wire_values, push them onto the stack
        variable_names = [v for v in next_instruction.variables[:-1] if not v.isnumeric()]
        values = [wire_values.get(v) for v in variable_names]
        if not all(values):
            for val, var in zip(values, variable_names):
                if val is None and var not in stack:
                    stack.push(instructions[var])
        else:
            # We have all data necessary to execute the next instruction!
            if next_instruction.command == 'SET':
                if next_instruction.value is None:
                    wire_values[next_instruction.sets] = wire_values[next_instruction.variables[0]]
                else:
                    wire_values[next_instruction.sets] = next_instruction.value
            elif next_instruction.command == 'AND':
                v = next_instruction.variables
                # First AND variable may be integer 1
                if v[0].isnumeric():
                    lhs = int(v[0])
                else:
                    lhs = wire_values[v[0]]
                rhs = wire_values[v[1]]
                wire_values[next_instruction.sets] = lhs & rhs
            elif next_instruction.command == 'OR':
                v = next_instruction.variables
                lhs = wire_values[v[0]]
                rhs = wire_values[v[1]]
                wire_values[next_instruction.sets] = lhs | rhs
            elif next_instruction.command == 'LSHIFT':
                lhs = wire_values[next_instruction.variables[0]]
                wire_values[next_instruction.sets] = lhs << next_instruction.value
            elif next_instruction.command == 'RSHIFT':
                lhs = wire_values[next_instruction.variables[0]]
                wire_values[next_instruction.sets] = lhs >> next_instruction.value
            elif next_instruction.command == 'NOT':
                v = wire_values[next_instruction.variables[0]]
                # Force v to be 16 bits
                wire_values[next_instruction.sets] = ~v & 0xffff
            else:
                raise Exception(f'Invalid command {next_instruction.command} found')
            print(f'popping stack')
            print(stack.stack.pop())
#            instructions.pop(next_instruction.sets)


if __name__ == '__main__':
    filepath = sys.argv[1]
    with open(filepath) as f:
        data = f.read()

    instructions = parse_input(data)

    wire_values = {}
    process(instructions, wire_values)

    print('Wire value of a is', wire_values['a'])
