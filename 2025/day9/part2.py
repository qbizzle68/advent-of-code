import sys
import itertools


def import_data(filepath: str) -> tuple[list[int], list[int]]:
    with open(filepath) as f:
        raw_data = f.readlines()

    x_vals, y_vals = zip(*tuple(map(int, d.rstrip().split(',')) for d in raw_data))
    return x_vals, y_vals


def build_layout(x_vals: list[int], y_vals: list[int]) -> list[list[int]]:
    # This was a bit confusing but for debugging ease we should build the
    # layout like the textual images accompanying the examples. This means
    # that y values map to rows and x values map to columns.

    row_count = max(y_vals) + 1
    col_count = max(x_vals) + 1

    layout = [None] * row_count
    for i in range(row_count):
        layout[i] = [0] * col_count

    # i is for row so iterate over y values
    for i in range(len(y_vals)):
        cur_row, cur_col = y_vals[i], x_vals[i]
        prev_row, prev_col = y_vals[i - 1], x_vals[i - 1]

        layout[cur_row][cur_col] = 1
        if cur_row == prev_row:
            min_col, max_col = (cur_col, prev_col) if cur_col < prev_col\
                                                   else (prev_col, cur_col)
            for j in range(min_col + 1, max_col):
                layout[cur_row][j] = 1
        else:
            assert cur_col == prev_col, f'Found non-consecutive coordinates ({cur_row},{cur_col}), ({prev_row},{prev_col})'
            min_row, max_row = (cur_row, prev_row) if cur_row < prev_row\
                                                   else (prev_row, cur_row)
            for j in range(min_row + 1, max_row):
                layout[j][cur_col] = 1

    # The following godforsaken code will go through the layout array
    # and also fill in all spaces inside of the shape. The general idea
    # is start from one direction (below goes from left to right) for a
    # given column/row and track the number of edges you've come across.
    # If the number is odd you're inside the shape and can fill the area.
    # The biggest complexity is moving along edges as some should signal
    # being inside the shape it some circumstances and outside in others.
    # The logic isn't so insainely hard to follow but it definitely
    # requires really thinking about every possible situation to truely
    # understand it.

    # todo: I think a way to improve this is replace layout with a set of coordinates
    # that make up the shape. Don't know if that will be any faster than summing the
    # values since we still have to iterate over all possible coordinates anyway

    def find_next_one(row: list[int], after: int) -> int | None:
        # Return the index of the next 1 after `after` or `None`
        # if none is found
        ptr = after + 1
        try:
            while row[ptr] != 1:
                ptr += 1
        except IndexError:
            return None
        
        return ptr
    
    def find_next_zero(row: list[int], after: int) -> int | None:
        # Same as `find_next_one()` but with 0.
        ptr = after + 1
        try:
            while row[ptr] != 0:
                ptr += 1
        except IndexError:
            return None
        
        return ptr

    # We are certain we won't add anything on the first or last rows
    for i in range(1, row_count - 1):
        ptr = 0
        row = layout[i]
        edges = 0
        # Also are certain we won't add anything on the first or last
        # columns but we do need to start at zero as that column can
        # still have an effect
        while ptr < col_count - 1:

            # Beginning of a horizontal edge
            if row[ptr] == 1 and row[ptr + 1] == 1:
                next_zero = find_next_zero(row, ptr)
                if next_zero is None:
                    break
                last_one = next_zero - 1
            
                #                         _ 
                # Edge looks like |_| or | | so don't want to insert anything
                if (layout[i - 1][ptr] == 1 and layout[i - 1][last_one] == 1 or
                    layout[i + 1][ptr] == 1 and layout[i + 1][last_one] == 1):
                    # Adding 2 to edges keeps the current state
                    edges += 2
                    # Move pointer AFTER last_one and not last_one or we'll trigger
                    # another edge.
                    ptr = last_one + 1
                    continue
                #                  _|  |_
                # Edge looks like |  or  | so we want to extend 1's depending
                # on edges
                elif (layout[i - 1][ptr] == 1 and layout[i + 1][last_one] == 1 or
                      layout[i + 1][ptr] == 1 and layout[i - 1][last_one] == 1):
                    # If we were outside shape we are now inside and vice-versa.
                    edges += 1
                    # Setting ptr to last_one will trigger another edge on next iteration
                    ptr = last_one + 1
                    continue
            # Vertical line which flips whether we're inside or outside the shape
            elif row[ptr] == 1 and row[ptr + 1] == 0:
                edges += 1
                ptr += 1
            
            # An odd number of edges means we're inside the shape, set inner values.
            if edges % 2 == 1:
                next_one = find_next_one(row, ptr)
                # we should be guaranteed to find a 1 i think
                assert next_one is not None, f'Something went wrong in row {i}'
                for j in range(ptr, next_one):
                    # So setting the inner values equal to 1 will mess with the logic
                    # above about distinguishing the type of horizontal line (arms
                    # up/down vs different directions). The simplest approach is put
                    # another value not equal to 1 or 0 to signal it's been changed
                    # but to disambiguate from the outer edges of the shape. Later
                    # replace all 2's with 1's.
                    row[j] = 2
                ptr = next_one
                continue
            else:
                # I think ptr should be pointing to a zero here so find the
                # the next 1
                next_one = find_next_one(row, ptr)
                if next_one is None:
                    break
                ptr = next_one

    # All inner values were set to 2 (see above). Change them to 1's.
    for i in range(row_count):
        for j in range(col_count):
            if layout[i][j] == 2:
                layout[i][j] = 1
            
    return layout


def plot_layout(layout: list[list[int]]) -> None:
    import matplotlib.pyplot as plt
    x = []
    y = []
    for i in range(len(layout)):
        for j in range(len(layout[0])):
            if layout[i][j] == 1:
                # See `build_layout()` for why i -> y and j -> x
                x.append(j)
                y.append(i)

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'ro', markersize=8, label='Points')
    ax = plt.gca()
    ax.invert_yaxis()

    plt.xlabel('X', fontsize=12)
    plt.ylabel('Y', fontsize=12)
    plt.title('Compressed Coordinate Layout', fontsize=14)
    plt.grid(True)

    plt.tight_layout()
    plt.show()


def main(x_vals: list[int], y_vals: list[int]) -> int:
    # First compress the 2d coordinates
    x_sorted = sorted(set(x_vals))
    y_sorted = sorted(set(y_vals))

    x_rank_map = {x: rank for rank, x in enumerate(x_sorted)}
    y_rank_map = {y: rank for rank, y in enumerate(y_sorted)}

    x_comp = tuple(x_rank_map[x] for x in x_vals)
    y_comp = tuple(y_rank_map[y] for y in y_vals)

    # Note: in the example-input.txt there's a quirky thing that happens
    # due to how small the layout is. Basically the only other cell that
    # needs to be filled in doesn't. If running the example code the
    # commented line below needs to be uncommented.
    layout = build_layout(x_comp, y_comp)
    # layout[1][2] = 1

    # Need a mapping of x_comp to x_vals and y_comp to y_vals. Then we
    # can check for all combinations of x_comp and y_comp that are valid in
    # layout and find the real coordinates in x_vals and y_vals and compute
    # the area. 
    x_reverse_map = {rank: x for rank, x in enumerate(x_sorted)}
    y_reverse_map = {rank: y for rank, y in enumerate(y_sorted)}

    coords = tuple(zip(x_comp, y_comp))
    max_area = 0
    for (x0, y0), (x1, y1) in itertools.combinations(coords, 2):
        if (x0, y0) == (x1, y1):
            continue
        # Check validity:
        # If the number of points in the square is equal to the count of values in
        # layout then the square lies entirely in the valid zone.
        expected_count = (abs(x1 - x0) + 1) * (abs(y1 - y0) + 1)
        min_x, max_x = (x0, x1) if x0 < x1 else (x1, x0)
        min_y, max_y = (y0, y1) if y0 < y1 else (y1, y0)
        true_count = sum(sum(row[min_x:max_x + 1]) for row in layout[min_y:max_y + 1])

        if true_count < expected_count:
            continue

        real_x0 = x_reverse_map[x0]
        real_x1 = x_reverse_map[x1]
        real_y0 = y_reverse_map[y0]
        real_y1 = y_reverse_map[y1]

        area = (abs(real_x1 - real_x0) + 1) * (abs(real_y1 - real_y0) + 1)
        if area > max_area:
            max_area = area

    return max_area


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} FILEPATH')
    filepath = sys.argv[1]

    x_vals, y_vals = import_data(filepath)
    result = main(x_vals, y_vals)
    print(f'Result is {result}')
    exit(0)
