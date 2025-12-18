import sys
import re


def import_data(filepath: str) -> dict:
    with open(filepath) as f:
        data = f.read()
    chunks = data.split('\n\n')

    data = {'shapes': [], 'regions': []}
    # Parse shapes
    # going to be tulpes of (area, space) where area is the area the shape's
    # profile and space is how much actual area it takes up
    for chunk in chunks[:-1]:
        space = chunk.count('#')
        area = space + chunk.count('.')
        data['shapes'].append({'area': area, 'space': space})

    # Parse regions
    regex = re.compile('([0-9]+)x([0-9]+)')
    for line in chunks[-1].splitlines():
        dims, indices = line.split(' ', maxsplit=1)
        dims = dims[:-1]

        match = regex.search(dims)
        if match is None:
            raise Exception(f'Unable to parse dimensions from {dims}')

        width, length = tuple(map(int, match.groups()))
        idx = tuple(map(int, indices.split(' ')))

        data['regions'].append({'width': width, 'height': length, 'indices': idx})

    return data 


def main(data) -> result:
    # Find how many inputs cannot fit no matter what strictly based on area
    shapes = data['shapes']
    regions = data['regions']
    valid_inputs = 0
    for region in regions:
        region_area = region['width'] * region['height']
        area = 0
        for i, quantity in enumerate(region['indices']):
            area += shapes[i]['space'] * quantity

        if area <= region_area:
            valid_inputs += 1

    return valid_inputs
    

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} FILEPATH')
    filepath = sys.argv[1]

    data = import_data(filepath)
    result = main(data)
    print(f'Result is {result}')
    exit(0)
