"""
LeetCode 217 -- Contains Duplicate
===================================
Given an integer array nums, return true if any value appears
at least twice in the array, and return false if every element is distinct.

Example:
    Input:  [1,2,3,1]
    Output: True

Approaches: set, sorting.
"""


def contains_duplicate_set(nums):
    """
    Approach 1: Use a set.
    Time: O(n), Space: O(n)
    """
    return len(nums) != len(set(nums))


def contains_duplicate_early_exit(nums):
    """
    Approach 2: Set with early exit.
    Time: O(n), Space: O(n)
    """
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False


def contains_duplicate_sort(nums):
    """
    Approach 3: Sort and check adjacent.
    Time: O(n log n), Space: O(1) if in-place sort
    """
    nums_sorted = sorted(nums)
    for i in range(1, len(nums_sorted)):
        if nums_sorted[i] == nums_sorted[i - 1]:
            return True
    return False


# ============================================================
# TESTS
# ============================================================

if __name__ == "__main__":
    for func in [contains_duplicate_set, contains_duplicate_early_exit, contains_duplicate_sort]:
        assert func([1, 2, 3, 1]) == True
        assert func([1, 2, 3, 4]) == False
        assert func([1, 1, 1, 3, 3, 4, 3, 2, 4, 2]) == True
        assert func([]) == False
        assert func([1]) == False

    print("All test cases passed")
