import sys
import pprint


def main(path: str) -> int:
    with open(path) as f:
        data = f.read().splitlines()

    map_ = ['.' * (len(data[0]) + 2)]
    for d in data:
        map_.append('.' + d + '.')
    map_.append('.' * (len(data[0]) + 2))

    accumulator = 0
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
                accumulator += 1

    print("There are", accumulator, "rolls that can be accessed")


if __name__ == '__main__':
    path = sys.argv[1]
    main(path)
    exit(0)
