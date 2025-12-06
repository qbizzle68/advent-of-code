import sys

data = sys.stdin.read()
unbuffered_lines = data.splitlines()
# add a sentinel value at the start of each line (we'll be working backwards from right to left
lines = [' ' + l for l in unbuffered_lines]

instruction_line = lines.pop()
instructions = tuple((c for c in instruction_line.split(' ') if c != ''))

instruction_pointer = len(instructions) - 1
accum = 0
numbers = []
for i in range(len(lines[0])-1, -1, -1):
    num_as_string=''
    for row in lines:
        if row[i] == ' ':
            continue
        num_as_string += row[i]
#    print(f"num_as_string = {num_as_string}")
#    print(f'numbers = {numbers}')
    if num_as_string == '':
        # compute value, move instruction pointer, update accum
        instruction = instructions[instruction_pointer]
#        print(f'instruction = {instruction}')
        if instruction == '+':
            tmp = 0
        else:
            tmp = 1

        for num in numbers:
            if instruction == '+':
                tmp += num
            else:
                tmp *= num
#        print(f'finished val = {tmp}')

        instruction_pointer -= 1
        accum += tmp
        numbers = []
    else:
        numbers.append(int(num_as_string))

print(accum)
