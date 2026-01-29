import sys
import itertools
import math
from collections import defaultdict


# So this absolutely works, but is ungodly slow. This took 
# between 30 - 60 minutes, probably much closer to an hour
# to compute. Not really sure how to speed this up but there
# must be a way.


def is_prime(val: int) -> bool:
    i = 2
    while i * i <= val:
        if val % i == 0:
            return False
        i += 1

    return True


class DefaultKeyDict(defaultdict):
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        value = self.default_factory(key)
        self[key] = value
        return value


prime_memos = DefaultKeyDict(is_prime)
decomp_memos = {}
def generate_prime_decomposition(val: int) -> list[tuple[int, int]]:
    decomposition = defaultdict(int)

    divisor = 2
    while val > 1:
        if val in decomp_memos:
            for k, v in decomp_memos[val]:
                decomposition[k] += v
            # want to divide val by val which will always equal 1
            val = 1
        else:
            if prime_memos[divisor] and val % divisor == 0:
                while val % divisor == 0:
                    decomposition[divisor] += 1
                    val /= divisor
            else:
                divisor += 1

    if val not in decomp_memos:
        decomp_memos[val] = decomposition

    return decomposition


def compute_gift_count(house: int) -> int:
    cache = {}

    # We're dealing with a sum of divisors here, which just follows a
    # geometric series. Therefore we sum the powers for each prime
    # divisor (e.g. 2^0 + 2^1 + 2^2 ...) for the count of that divisor
    # in the prime factorization. The multiply all of these values
    # for each unique prime number in the factorization and that is the
    # sum of all divisors for `house` number.

    def wrapper() -> int:
        decomposition = generate_prime_decomposition(house)
        product = 1
        for k, v in decomposition.items():
            val = cache.get((k, v))
            if val is not None:
                product *= val
            else:
                tmp = ((k ** (v + 1) - 1) // (k - 1))
                product *= tmp
                cache[(k, v)] = tmp

        return product * 10

    return wrapper()


def main(count: int, start: int = 1) -> int:
    candidate = start
    while True:
        gift_count = compute_gift_count(candidate)
        print(f'House {candidate} got {gift_count} presents')
        if gift_count >= count:
            break
        candidate += 1

    return candidate
               

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} COUNT [START]')
    count = int(sys.argv[1])
    if len(sys.argv) == 3:
        start = int(sys.argv[2])
    else:
        start = 0

    result = main(count, start)
    print(f'Result is {result}')
