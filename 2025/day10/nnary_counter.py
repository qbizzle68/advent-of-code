from itertools import combinations_with_replacement

class NnaryCounter:
    """
    Iterator that generates lists of length n with values 0-9,
    ordered by the sum of their elements (smallest sum first).
    """
    def __init__(self, length, start_value=0, max_value=9):
        self.length = length
        self.max_value = max_value
        # self.current_sum = 0
        self.current_sum = int(start_value)
        self.max_sum = length * max_value
        
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current_sum > self.max_sum:
            raise StopIteration
        
        # Generate all combinations for the current sum
        if not hasattr(self, '_current_combinations'):
            self._current_combinations = list(self._generate_combinations_for_sum(self.current_sum))
            self._combo_index = 0
        
        # Return next combination from current sum
        if self._combo_index < len(self._current_combinations):
            result = self._current_combinations[self._combo_index]
            self._combo_index += 1
            return result
        
        # Move to next sum
        self.current_sum += 1
        if self.current_sum > self.max_sum:
            raise StopIteration
        
        self._current_combinations = list(self._generate_combinations_for_sum(self.current_sum))
        self._combo_index = 0
        
        if self._current_combinations:
            result = self._current_combinations[0]
            self._combo_index = 1
            return result
        else:
            return self.__next__()
    
    def _generate_combinations_for_sum(self, target_sum):
        """Generate all ways to distribute target_sum across self.length positions."""
        def backtrack(remaining_sum, position, current):
            if position == self.length:
                if remaining_sum == 0:
                    yield current[:]
                return
            
            # Try values from 0 to min(remaining_sum, max_value)
            for val in range(min(remaining_sum, self.max_value) + 1):
                current.append(val)
                yield from backtrack(remaining_sum - val, position + 1, current)
                current.pop()
        
        yield from backtrack(target_sum, 0, [])


def nnary_counter(length, max_value=9):
    """
    Generator function that yields lists of specified length with values 0-max_value,
    ordered by sum (smallest sum first).
    
    Args:
        length: Length of the lists to generate
        max_value: Maximum value for each position (default 9)
    
    Yields:
        Lists of integers where sum increases monotonically
    
    Example:
        >>> for val in nnary_counter(3):
        ...     print(val)
        [0, 0, 0]
        [1, 0, 0]
        [0, 1, 0]
        [0, 0, 1]
        [2, 0, 0]
        ...
    """
    return NnaryCounter(length, max_value)


# Example usage
if __name__ == "__main__":
    print("First 20 values for length=3:")
    counter = nnary_counter(3)
    for i, val in enumerate(counter):
        if i >= 20:
            break
        print(f"Sum={sum(val)}: {val}")
    
    print("\n" + "="*40)
    print("All values with sum <= 2 for length=3:")
    counter = nnary_counter(3)
    for val in counter:
        if sum(val) > 2:
            break
        print(val)
