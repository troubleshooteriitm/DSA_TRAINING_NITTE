"""
LeetCode 283 -- Move Zeroes
=============================
Given an integer array nums, move all 0's to the end while
maintaining the relative order of the non-zero elements.
Must be done in-place.

Example:
    Input:  [0,1,0,3,12]
    Output: [1,3,12,0,0]

Approach: Two-pointer -- slow tracks next non-zero position.
Time: O(n), Space: O(1)
"""


def move_zeroes(nums):
    """Two-pointer approach."""
    slow = 0  # Position to place next non-zero

    for fast in range(len(nums)):
        if nums[fast] != 0:
            nums[slow], nums[fast] = nums[fast], nums[slow]
            slow += 1


def move_zeroes_v2(nums):
    """Alternative: overwrite then fill zeros."""
    pos = 0

    # Move all non-zero to front
    for num in nums:
        if num != 0:
            nums[pos] = num
            pos += 1

    # Fill remaining with zeros
    while pos < len(nums):
        nums[pos] = 0
        pos += 1


# ============================================================
# TESTS
# ============================================================

if __name__ == "__main__":
    for func in [move_zeroes, move_zeroes_v2]:
        nums = [0, 1, 0, 3, 12]
        func(nums)
        assert nums == [1, 3, 12, 0, 0], f"Test 1 failed: {nums}"

        nums = [0]
        func(nums)
        assert nums == [0], f"Test 2 failed: {nums}"

        nums = [1]
        func(nums)
        assert nums == [1], f"Test 3 failed: {nums}"

        nums = [0, 0, 0, 1]
        func(nums)
        assert nums == [1, 0, 0, 0], f"Test 4 failed: {nums}"

        nums = [1, 2, 3]
        func(nums)
        assert nums == [1, 2, 3], f"Test 5 failed: {nums}"

    print("All test cases passed")
