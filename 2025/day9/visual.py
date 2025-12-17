import sys

import matplotlib.pyplot as plt


def import_data(filepath: str) -> tuple[list[int], list[int]]:
    with open(filepath) as f:
        raw_data = f.readlines()

    x_vals, y_vals = zip(*tuple(map(int, d.rstrip().split(',')) for d in raw_data))
    return x_vals, y_vals


def plot(x_vals: list[int], y_vals: list[int]) -> None:
    # Create the plot
    plt.figure(figsize=(10, 6))
    
    # Plot green lines connecting the points
    # need to add first element again to connect last segment
    plt.plot(x_vals + (x_vals[0],), y_vals + (y_vals[0],), 'g-', linewidth=2, label='Path')

    # Plot red points
    plt.plot(x_vals, y_vals, 'ro', markersize=8, label='Points')
    ax = plt.gca()
    ax.invert_yaxis()

    # Add labels and title
    plt.xlabel('X', fontsize=12)
    plt.ylabel('Y', fontsize=12)
    plt.title('Coordinate Plot', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Display the plot
    plt.tight_layout()
    plt.show()


def compress_coordinates(x_vals: list[int], y_vals: list[int]) -> tuple[list[int], list[int]]:
    x_sorted = sorted(set(x_vals))
    y_sorted = sorted(set(y_vals))

    x_map = {x: rank for rank, x in enumerate(x_sorted)}
    y_map = {y: rank for rank, y in enumerate(y_sorted)}

    x_compressed = tuple(x_map[x] for x in x_vals)
    y_compressed = tuple(y_map[y] for y in y_vals)

    return x_compressed, y_compressed


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage {sys.argv[0]} FILEPATH')
    filepath = sys.argv[1]

    x_vals, y_vals = import_data(filepath)
    x_comp, y_comp = compress_coordinates(x_vals, y_vals)
    #plot(x_vals, y_vals)
    plot(x_comp, y_comp)
    exit(0)
