import sys
import pprint


# This is to hash the array map, nothing to do with a hashmap structure.
def hash_map(map_: list[list[str]]) -> int:
    hash_ = 123453
    for row in map_:
        for col in row:
            hash_ = hash((col, hash_))

    return hash_


def main(path: str) -> int:
    with open(path) as f:
        data = f.read().splitlines()

    map_ = [['.' for _ in range(len(data[0]) + 2)]]
    for row in data:
        map_.append(['.'] + [c for c in row] + ['.'])
    map_.append(['.' for _ in range(len(data[0]) + 2)])

    old_hash = 1 
    while (tmp:= hash_map(map_)) != old_hash:
        old_hash = tmp
        for i in range(1, len(map_) - 1):
            for j in range(1, len(map_[0]) - 1):
                if map_[i][j] != '@':
                    continue
                count = 0
                if map_[i-1][j-1] == '@': count+=1
                if map_[i-1][j] == '@': count+=1
                if map_[i-1][j+1] == '@': count+=1
                if map_[i][j-1] == '@': count+=1
                if map_[i][j+1] == '@': count+=1
                if map_[i+1][j-1] == '@': count+=1
                if map_[i+1][j] == '@': count+=1
                if map_[i+1][j+1] == '@': count+=1
                if count < 4:
                    map_[i][j] = 'x'

    accumulator=0
    for row in map_:
        for col in row:
            if col == 'x':
                accumulator += 1

    print("There are", accumulator, "rolls that can be accessed")


if __name__ == '__main__':
    path = sys.argv[1]
    main(path)
    exit(0)
