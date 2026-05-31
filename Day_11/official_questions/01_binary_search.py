"""
LeetCode 704 -- Binary Search
==============================
Given a sorted array of integers nums and a target, return the index
if found, else return -1.

Example:
    Input:  nums = [-1,0,3,5,9,12], target = 9
    Output: 4

Time: O(log n), Space: O(1)
"""


def binary_search_iterative(nums, target):
    """Iterative binary search."""
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2  # Avoid overflow

        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


def binary_search_recursive(nums, target, left=None, right=None):
    """Recursive binary search."""
    if left is None:
        left, right = 0, len(nums) - 1

    if left > right:
        return -1

    mid = left + (right - left) // 2

    if nums[mid] == target:
        return mid
    elif nums[mid] < target:
        return binary_search_recursive(nums, target, mid + 1, right)
    else:
        return binary_search_recursive(nums, target, left, mid - 1)


# ============================================================
# TESTS
# ============================================================

if __name__ == "__main__":
    for func in [binary_search_iterative, binary_search_recursive]:
        assert func([-1, 0, 3, 5, 9, 12], 9) == 4
        assert func([-1, 0, 3, 5, 9, 12], 2) == -1
        assert func([5], 5) == 0
        assert func([5], 3) == -1
        assert func([], 3) == -1
        assert func([1, 2, 3, 4, 5], 1) == 0   # First element
        assert func([1, 2, 3, 4, 5], 5) == 4   # Last element

    print("All test cases passed")
