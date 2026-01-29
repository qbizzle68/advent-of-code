import sys
import re
from collections import defaultdict


class Instruction:
    def __init__(self, registers: dict[str, float]) -> None:
        self.registers = registers


class HalfInstruction(Instruction):
    def __init__(self, registers: dict[str, float], register: str) -> None:
        super().__init__(registers)
        self.reg = register

    def __call__(self) -> int:
        self.registers[self.reg] /= 2.0
        return 1
    
    def __str__(self) -> str:
        return f'hlf {self.reg}'
    

class IncrementInstruction(Instruction):
    def __init__(self, registers: dict[str, float], register: str) -> None:
        super().__init__(registers)
        self.reg = register

    def __call__(self) -> int:
        self.registers[self.reg] += 1
        return 1
    
    def __str__(self) -> str:
        return f'inc {self.reg}'


class TripleInstruction(Instruction):
    def __init__(self, registers: dict[str, float], register: str) -> None:
        super().__init__(registers)
        self.reg = register

    def __call__(self) -> int:
        self.registers[self.reg] *= 3.0
        return 1
    
    def __str__(self) -> str:
        return f'tpl {self.reg}'


class JumpInstruction(Instruction):
    def __init__(self, registers: dict[str, float], count: int,
                 register: str | None = None, if_even: bool | None = None)\
                    -> None:
        super().__init__(registers)
        self.count = count
        self.reg = register
        self.if_even = if_even

    def __call__(self) -> int:
        if self.if_even is None:
            return self.count
        elif self.if_even is True:
            return self.count if self.registers[self.reg] % 2 == 0 else 1
        elif self.if_even is False:
            return self.count if self.registers[self.reg] == 1 else 1
        raise ValueError(f'self.if_even ({self.if_even}) unexpected value')
    
    def __str__(self) -> str:
        if self.if_even is None:
            return f'jmp {self.count}'
        elif self.if_even is True:
            return f'jie {self.reg}, {self.count}'
        elif self.if_even is False:
            return f'jio {self.reg}, {self.count}'
        

class CPU:
    def __init__(self, registers: dict[str, int], instructions: list[Instruction]) -> None:
        self.registers = registers
        self.instructions = instructions
        self.rsp = 0
        # self.count as the maximum index we can reach
        self.count = len(instructions) - 1

    def __call__(self) -> None:
        while self.rsp >= 0 and self.rsp <= self.count:
            self.rsp += self.instructions[self.rsp]()


def import_instructions(path: str, registers: dict[str, int]) -> list[Instruction]:
    with open(path) as f:
        data = f.readlines()

    instructions = []
    broad_regex = re.compile('^(hlf|tpl|inc|jmp|jie|jio).+$')
    for line in data:
        match = broad_regex.match(line)
        if match is None:
            raise ValueError(f'unable to parse {line}')
        
        if match.group(1) == 'hlf':
            mmatch = re.match('hlf ([ab])', match.group(0))
            if mmatch is None:
                raise ValueError(f'unable to parse hlf instruction {line}')
            instruction = HalfInstruction(registers, mmatch.group(1))
        elif match.group(1) == 'tpl':
            mmatch = re.match('tpl ([ab])', match.group(0))
            if mmatch is None:
                raise ValueError(f'unable to parse tpl instruction {line}')
            instruction = TripleInstruction(registers, mmatch.group(1))
        elif match.group(1) == 'inc':
            mmatch = re.match('inc ([ab])', match.group(0))
            if mmatch is None:
                raise ValueError(f'unable to parse inc instruction {line}')
            instruction = IncrementInstruction(registers, mmatch.group(1))
        elif match.group(1) == 'jmp':
            mmatch = re.match(r'jmp ([+-]\d+)', match.group(0))
            if mmatch is None:
                raise ValueError(f'unable to parse jmp instruction {line}')
            instruction = JumpInstruction(registers, int(mmatch.group(1)), None, None)
        elif match.group(1) == 'jie':
            mmatch = re.match(r'jie ([ab]), ([+-]\d+)', match.group(0))
            if mmatch is None:
                raise ValueError(f'unable to parse jie instruction {line}')
            instruction = JumpInstruction(registers, int(mmatch.group(2)), mmatch.group(1), True)
        elif match.group(1) == 'jio':
            mmatch = re.match(r'jio ([ab]), ([+-]\d+)', match.group(0))
            if mmatch is None:
                raise ValueError(f'unable to parse jio instruction {line}')
            instruction = JumpInstruction(registers, int(mmatch.group(2)), mmatch.group(1), False)
        
        instructions.append(instruction)
    
    return instructions


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'Usage: {sys.argv[0]} INPUT_PATH A_START')
    path = sys.argv[1]
    a_initial_value = int(sys.argv[2])
    registers = {'a': a_initial_value, 'b': 0}
    instructions = import_instructions(path, registers)
    cpu = CPU(registers, instructions)
    cpu()

    print(f'result is {cpu.registers['b']}')
