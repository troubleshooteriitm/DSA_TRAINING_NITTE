"""
LeetCode 169 -- Majority Element
=================================
Given an array nums of size n, return the majority element.
The majority element is the element that appears more than n / 2 times.

Example:
    Input:  [3,2,3]
    Output: 3

Approaches: Counter, sorting, Boyer-Moore Voting Algorithm.
"""

from collections import Counter


def majority_element_counter(nums):
    """
    Approach 1: Counter (hash map).
    Time: O(n), Space: O(n)
    """
    count = Counter(nums)
    return count.most_common(1)[0][0]


def majority_element_sort(nums):
    """
    Approach 2: Sort -- middle element is always the majority.
    Time: O(n log n), Space: O(1)
    """
    nums.sort()
    return nums[len(nums) // 2]


def majority_element_boyer_moore(nums):
    """
    Approach 3: Boyer-Moore Voting Algorithm.
    Time: O(n), Space: O(1) -- OPTIMAL

    Intuition: The majority element's count will always survive
    the cancellation process because it appears > n/2 times.
    """
    candidate = None
    count = 0

    for num in nums:
        if count == 0:
            candidate = num
        count += 1 if num == candidate else -1

    return candidate


# ============================================================
# TESTS
# ============================================================

if __name__ == "__main__":
    for func in [majority_element_counter, majority_element_boyer_moore]:
        assert func([3, 2, 3]) == 3
        assert func([2, 2, 1, 1, 1, 2, 2]) == 2
        assert func([1]) == 1
        assert func([1, 1, 1]) == 1

    # Sort modifies in-place, test separately
    assert majority_element_sort([3, 2, 3]) == 3
    assert majority_element_sort([2, 2, 1, 1, 1, 2, 2]) == 2

    print("All test cases passed")
