import sys
import re
import math
import itertools


class ButtonIterator:
    """Custom iterator class that controls how a list of buttons is iterated over.
    The iterator is the result of permutations of buttons of incrementally
    increasing length, up to the length of the list. This iterable however does
    not create lists that press a button more than once. As the result from this
    script produced the correct result, this functionality (thank god) obviously
    wasn't needed, and permutations of buttons occuring only once suffices.
    """

    def __init__(self, vals: list, safety_max: int = 5) -> None:
        self.vals = vals
        self.max = safety_max
        self._generator = itertools.chain.from_iterable(
            itertools.permutations(self.vals, i)
            for i in range(1, self.max)
        )

    def __iter__(self) -> 'NewCounter':
        return self

    def __next__(self) -> list[int]:
        try:
            return next(self._generator)
        except StopIteration:
            raise ValueError('Hit safety maximum of {self.max} for {self.vals}') from None


def parse_input(filepath: str) -> list[dict]:
    """Parse the input from `filepath` into a list of dictionaries representing
    machine like objects. Each machine has a `light`, `buttons`, and `joltage`
    key, where the light is a list of boolean values for which indicator light
    should be on, buttons is a list of tuples where each tuple is which light
    that button toggles, and joltage is a list of joltages not used for part 1.
    """
    with open(filepath) as f:
        data = f.readlines()

    machines = []
    regex = re.compile(r'\([0-9]+(,[0-9]+)*\)')
    for d in data:
        match = re.search(r'\[(.*)\]', d)
        if match is None:
            raise Exception(f'Unable to parse indicator lights for {d}')
        lights = [True if c == '#' else False for c in match.group(1)]
        machine = {'lights': lights, 'buttons': []}

        match = re.findall(r'\([0-9]+(?:,[0-9]+)*\)', d)
        if match == []:
            raise Exception(f'Unable to parse button directinos for {d}')
        for m in match:
            numbers = re.findall('[0-9]+', m)
            machine['buttons'].append(tuple(map(int, numbers)))

        tmp = re.search(r'\{([0-9]+(?:,[0-9]+)+)\}', d)
        if tmp is None:
            raise Exception(f'Unable to parse joltage for {d}')
        match = re.findall('[0-9]+', tmp[0])
        machine['joltage'] = tuple(map(int, match[:]))

        machines.append(machine)
    
    return machines


def main(data: list) -> int:
    """The idea here is create increasing length iterables of buttons to press
    starting at 1 and ending with the number of buttons for each machine. This
    ensures we find the minimal number of button presses first, then we can break
    out of the loop and continue to the next machine. A list of boolean values
    is used to represent indicator lights, and each button press simple toggles
    the inicator light. The first time we find a match, due to the order of
    iterables from `ButtonIterator`, we have the minimum number of button presses
    and can add that number to an array and break out of the loop and begin
    processing the next machine.
    """

    button_presses = []
    for machine in data:
        for presses in ButtonIterator(machine['buttons'], len(machine['buttons']) + 1):
            machine_state = [False] * len(machine['lights'])
            for light_number in itertools.chain.from_iterable(presses):
                machine_state[light_number] = not machine_state[light_number]
            if machine_state == machine['lights']:
                button_presses.append(len(presses))
                break

    return sum(button_presses)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} FILEPATH')
    filepath = sys.argv[1]

    data = parse_input(filepath)
    result = main(data)
    print(f'Result is {result}')
