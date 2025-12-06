import sys
import itertools

if len(sys.argv) != 3:
    print(f'Usage: {sys.argv[0]} INPUT CYCLES')
input_ = sys.argv[1]
cycles = int(sys.argv[2])

# Convert the string into list of tuple pairs holding the data
result = []
chars = []
char_count = []
previous_char=''
i = -1
for c in input_:
    if c != previous_char:
        i += 1
        chars.append(c)
        char_count.append(0)
    char_count[i] += 1
    previous_char = c

for count, c in zip(char_count, chars):
    result.append((int(count), int(c)))

# Now result is of the form [(1, 1), (1, 2), (2, 1)] which corresponds to the string
# 111221 i.e. a list of (count, char) tuples
for num in range(1, cycles):
    buffer = []
    itr = itertools.chain.from_iterable(result)
    previous_char = next(itr)
    current_count = 1
    for char in itr:
        if char != previous_char:
            buffer.append((current_count, previous_char))
            current_count = 0
        current_count += 1

        previous_char = char
    buffer.append((current_count, char))
    result = buffer

output = ''.join(map(str, itertools.chain.from_iterable(result)))
print('Length of result =', len(output))

