import sys

data = sys.stdin.read().splitlines()

ranges = []
for d in data:
    if d == '':
        break
    vals = d.split('-')
    ranges.append((int(vals[0]), int(vals[1])))

ranges.sort()

# Combine ranges
condensed_ranges = []
stop = False
pointer = 0
while not stop:
    # Ranges should remain sorted, so we only need to compare a range with the next range.
    # If they overlap, conatin, or butt up against, they should be condensed and continue
    # to the next ranges. When no changes are made we're done. If a range can't be combined
    # with the next range then it should be considered condensed and added to the condensed
    # ranges.

#    print(f'pointer = {pointer}, len = {len(ranges)}')
    if pointer >= len(ranges) - 1:
        if pointer == len(ranges) - 1: # We didn't analyze the last element
            condensed_ranges.append(ranges[-1])
        if ranges == condensed_ranges:
            break
        ranges, condensed_ranges = condensed_ranges, []
 #       print('reseting pointer')
        pointer = 0
        continue

    r_start, r_end = ranges[pointer]
    compare_start, compare_end = ranges[pointer + 1]
    # Ranges butt up against eachother
    if (r_end == compare_start) or (r_end + 1 == compare_start):
        condensed_ranges.append((r_start, compare_end))
        pointer += 2
    # Range contains next
    elif compare_end <= r_end:
        # This appends the wider range (the one pointed to) and not the next, this basically
        # just deletes the next from original list
        condensed_ranges.append((r_start, r_end))
        pointer += 2
    # Ranges overlap
    elif compare_start <= r_end:
        condensed_ranges.append((r_start, compare_end))
        pointer += 2
    else:
        condensed_ranges.append((r_start, r_end))
        pointer += 1

#print(ranges)

accumulator = 0
for range_ in ranges:
    difference = range_[1] - range_[0] + 1
    accumulator += difference

print(f'Number of valid IDs is {accumulator}')
