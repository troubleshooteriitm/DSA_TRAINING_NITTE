"""
LeetCode 53 - Maximum Subarray

Problem:
    Given an integer array nums, find the subarray with the largest sum,
    and return its sum.

    A subarray is a contiguous non-empty sequence of elements within an array.

Example 1:
    Input: nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    Output: 6
    Explanation: The subarray [4, -1, 2, 1] has the largest sum 6.

Example 2:
    Input: nums = [1]
    Output: 1

Example 3:
    Input: nums = [5, 4, -1, 7, 8]
    Output: 23

Approach: Kadane's Algorithm
    - Maintain a running sum of the current subarray.
    - If the running sum becomes negative, reset it to 0 (start a new subarray).
    - Track the maximum sum seen so far.
    - Time Complexity: O(n)
    - Space Complexity: O(1)
"""

from typing import List


def max_subarray(nums: List[int]) -> int:
    """
    Find the contiguous subarray with the largest sum using Kadane's algorithm.

    Args:
        nums: List of integers.

    Returns:
        The maximum subarray sum.
    """
    # Initialize with the first element
    max_sum = nums[0]
    current_sum = nums[0]

    # Iterate from the second element onward
    for i in range(1, len(nums)):
        # Either extend the current subarray or start a new one
        current_sum = max(nums[i], current_sum + nums[i])

        # Update the global maximum
        max_sum = max(max_sum, current_sum)

    return max_sum


def max_subarray_with_indices(nums: List[int]) -> tuple:
    """
    Variant that also returns the start and end indices of the maximum subarray.

    Args:
        nums: List of integers.

    Returns:
        Tuple of (max_sum, start_index, end_index).
    """
    max_sum = nums[0]
    current_sum = nums[0]
    start = 0
    end = 0
    temp_start = 0

    for i in range(1, len(nums)):
        if nums[i] > current_sum + nums[i]:
            current_sum = nums[i]
            temp_start = i
        else:
            current_sum += nums[i]

        if current_sum > max_sum:
            max_sum = current_sum
            start = temp_start
            end = i

    return max_sum, start, end


#  Test Cases 

# Test 1: Standard case with mixed positive and negative numbers
assert max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6

# Test 2: Single element
assert max_subarray([1]) == 1

# Test 3: All positive numbers
assert max_subarray([5, 4, -1, 7, 8]) == 23

# Test 4: All negative numbers (pick the least negative)
assert max_subarray([-3, -2, -5, -1, -4]) == -1

# Test 5: Two elements
assert max_subarray([-2, 1]) == 1

# Test 6: Entire array is the max subarray
assert max_subarray([1, 2, 3, 4]) == 10

# Test 7: Single negative element
assert max_subarray([-1]) == -1

# Test 8: Large positive followed by large negatives
assert max_subarray([100, -1, -2, -3]) == 100

# Test 9: Variant with indices
result = max_subarray_with_indices([-2, 1, -3, 4, -1, 2, 1, -5, 4])
assert result[0] == 6  # max sum
assert result[1] == 3  # start index
assert result[2] == 6  # end index

print("All test cases passed!")
