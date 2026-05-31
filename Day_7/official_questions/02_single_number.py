"""
LeetCode 136 - Single Number

Problem:
    Given a non-empty array of integers `nums`, every element appears
    twice except for one. Find that single one.

    You must implement a solution with a linear runtime complexity
    and use only constant extra space.

Examples:
    Input: nums = [2, 2, 1]
    Output: 1

    Input: nums = [4, 1, 2, 1, 2]
    Output: 4

    Input: nums = [1]
    Output: 1

Constraints:
    - 1 <= nums.length <= 3 * 10^4
    - -3 * 10^4 <= nums[i] <= 3 * 10^4
    - Each element in the array appears exactly twice except for one
      element which appears exactly once.

Approach:
    XOR Bit Manipulation:
    - XOR of a number with itself is 0:  a ^ a = 0
    - XOR of a number with 0 is itself:  a ^ 0 = a
    - XOR is commutative and associative: order doesn't matter

    If we XOR all elements together, every pair cancels out (becomes 0),
    leaving only the single unique element.

    Example: [4, 1, 2, 1, 2]
        4 ^ 1 ^ 2 ^ 1 ^ 2
      = 4 ^ (1 ^ 1) ^ (2 ^ 2)
      = 4 ^ 0 ^ 0
      = 4
"""


def single_number(nums: list[int]) -> int:
    """
    Find the element that appears only once using XOR.

    Every element appears exactly twice except one. XOR-ing all
    elements together cancels out the pairs, leaving the unique one.

    Time Complexity: O(n) -- single pass through the array
    Space Complexity: O(1) -- only one variable used

    Args:
        nums: List of integers where every element appears twice
              except for exactly one element.

    Returns:
        The single element that does not have a duplicate.
    """
    result = 0

    for num in nums:
        # XOR each element with the running result.
        # Duplicates cancel out (x ^ x = 0), leaving the unique element.
        result ^= num

    return result


def single_number_reduce(nums: list[int]) -> int:
    """
    Alternative implementation using functools.reduce.

    Functionally identical to the loop approach, but uses
    Python's reduce for a more concise expression.

    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    from functools import reduce
    from operator import xor

    return reduce(xor, nums)


# ===== Test Cases =====

# Test Case 1: Single number at the end
assert single_number([2, 2, 1]) == 1
assert single_number_reduce([2, 2, 1]) == 1

# Test Case 2: Single number at the start
assert single_number([4, 1, 2, 1, 2]) == 4
assert single_number_reduce([4, 1, 2, 1, 2]) == 4

# Test Case 3: Array with single element
assert single_number([1]) == 1
assert single_number_reduce([1]) == 1

# Test Case 4: Negative numbers
assert single_number([-1, -1, -2]) == -2
assert single_number_reduce([-1, -1, -2]) == -2

# Test Case 5: Mix of positive and negative
assert single_number([1, -1, 1]) == -1
assert single_number_reduce([1, -1, 1]) == -1

# Test Case 6: Larger array
assert single_number([10, 3, 5, 3, 10, 5, 7]) == 7
assert single_number_reduce([10, 3, 5, 3, 10, 5, 7]) == 7

# Test Case 7: Zero is the single number
assert single_number([0, 1, 1]) == 0
assert single_number_reduce([0, 1, 1]) == 0

# Test Case 8: All same except one, larger values
assert single_number([100, 200, 100]) == 200
assert single_number_reduce([100, 200, 100]) == 200

print("All test cases passed!")
