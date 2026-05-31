"""
LeetCode 268 - Missing Number

Problem:
    Given an array `nums` containing n distinct numbers in the range [0, n],
    return the only number in the range that is missing from the array.

Examples:
    Input: nums = [3, 0, 1]
    Output: 2
    Explanation: n = 3 since there are 3 numbers, so all numbers are in
    the range [0, 3]. 2 is the missing number.

    Input: nums = [0, 1]
    Output: 2

    Input: nums = [9, 6, 4, 2, 3, 5, 7, 0, 1]
    Output: 8

Constraints:
    - n == nums.length
    - 1 <= n <= 10^4
    - 0 <= nums[i] <= n
    - All the numbers of nums are unique.

Approaches:
    1. Sum Formula (Gauss's formula) -- O(n) time, O(1) space
    2. XOR -- O(n) time, O(1) space
    3. Sorting -- O(n log n) time, O(1) space
"""


def missing_number_sum(nums: list[int]) -> int:
    """
    Approach 1: Sum Formula (Gauss's Formula).

    The sum of first n natural numbers is n * (n + 1) / 2.
    Subtract the actual sum of the array from this expected sum
    to get the missing number.

    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    n = len(nums)
    # Expected sum of numbers from 0 to n
    expected_sum = n * (n + 1) // 2
    # Actual sum of elements in the array
    actual_sum = sum(nums)
    # The difference is the missing number
    return expected_sum - actual_sum


def missing_number_xor(nums: list[int]) -> int:
    """
    Approach 2: XOR.

    XOR has two key properties:
      - a ^ a = 0  (any number XOR'd with itself is 0)
      - a ^ 0 = a  (any number XOR'd with 0 is itself)

    XOR all indices (0 to n) with all array elements.
    All paired numbers cancel out, leaving only the missing one.

    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    n = len(nums)
    xor_result = n  # Start with n (the last index value)

    for i in range(n):
        # XOR with both the index and the element at that index
        xor_result ^= i ^ nums[i]

    return xor_result


def missing_number_sort(nums: list[int]) -> int:
    """
    Approach 3: Sorting.

    Sort the array and check if each index matches its value.
    The first mismatch reveals the missing number.
    If no mismatch is found, the missing number is n.

    Time Complexity: O(n log n) -- due to sorting
    Space Complexity: O(1) -- if sorting is in-place
    """
    nums.sort()
    n = len(nums)

    for i in range(n):
        # If the value at index i doesn't match i, then i is missing
        if nums[i] != i:
            return i

    # If all indices match, the missing number is n
    return n


# ===== Test Cases =====

# Test Case 1: Missing number in the middle
assert missing_number_sum([3, 0, 1]) == 2
assert missing_number_xor([3, 0, 1]) == 2
assert missing_number_sort([3, 0, 1]) == 2

# Test Case 2: Missing number at the end
assert missing_number_sum([0, 1]) == 2
assert missing_number_xor([0, 1]) == 2
assert missing_number_sort([0, 1]) == 2

# Test Case 3: Larger array with missing number
assert missing_number_sum([9, 6, 4, 2, 3, 5, 7, 0, 1]) == 8
assert missing_number_xor([9, 6, 4, 2, 3, 5, 7, 0, 1]) == 8
assert missing_number_sort([9, 6, 4, 2, 3, 5, 7, 0, 1]) == 8

# Test Case 4: Missing 0
assert missing_number_sum([1]) == 0
assert missing_number_xor([1]) == 0
assert missing_number_sort([1]) == 0

# Test Case 5: Single element, missing 1
assert missing_number_sum([0]) == 1
assert missing_number_xor([0]) == 1
assert missing_number_sort([0]) == 1

# Test Case 6: Missing number at the end of a larger sequence
assert missing_number_sum([0, 1, 2, 3, 4]) == 5
assert missing_number_xor([0, 1, 2, 3, 4]) == 5
assert missing_number_sort([0, 1, 2, 3, 4]) == 5

print("All test cases passed!")
