"""
LeetCode 189 -- Rotate Array

Problem:
    Given an integer array `nums`, rotate the array to the right by `k` steps,
    where `k` is non-negative.

    Example 1:
        Input:  nums = [1,2,3,4,5,6,7], k = 3
        Output: [5,6,7,1,2,3,4]
        Explanation:
            rotate 1 step   [7,1,2,3,4,5,6]
            rotate 2 steps  [6,7,1,2,3,4,5]
            rotate 3 steps  [5,6,7,1,2,3,4]

    Example 2:
        Input:  nums = [-1,-100,3,99], k = 2
        Output: [3,99,-1,-100]

    Constraints:
        - 1 <= nums.length <= 10^5
        - -2^31 <= nums[i] <= 2^31 - 1
        - 0 <= k <= 10^5

    Follow up:
        - Try to come up with as many solutions as you can.
        - Could you do it in-place with O(1) extra space?

Approaches:
    1. Extra Array         -- O(n) time, O(n) space
    2. Reverse Approach    -- O(n) time, O(1) space   Optimal
    3. Cyclic Replacements -- O(n) time, O(1) space
"""

from typing import List


# ============================================================================
# Approach 1: Extra Array
# ============================================================================
def rotate_extra_array(nums: List[int], k: int) -> None:
    """
    Rotate array using an extra array.

    Strategy:
        - Create a new array where each element is placed at its
          rotated position: new_index = (old_index + k) % n.
        - Copy the result back into the original array.

    Time Complexity:  O(n)
    Space Complexity: O(n)
    """
    n = len(nums)
    k = k % n  # Handle k > n

    if k == 0:
        return

    # Place each element in its new position
    rotated = [0] * n
    for i in range(n):
        rotated[(i + k) % n] = nums[i]

    # Copy back to original array (in-place modification)
    for i in range(n):
        nums[i] = rotated[i]


# ============================================================================
# Approach 2: Reverse Approach (Optimal)
# ============================================================================
def rotate_reverse(nums: List[int], k: int) -> None:
    """
    Rotate array using the three-reverse technique.

    Strategy:
        Given nums = [1, 2, 3, 4, 5, 6, 7] and k = 3:

        Step 1: Reverse the entire array     [7, 6, 5, 4, 3, 2, 1]
        Step 2: Reverse the first k elements  [5, 6, 7, 4, 3, 2, 1]
        Step 3: Reverse the remaining n-k    [5, 6, 7, 1, 2, 3, 4]

    Why it works:
        Reversing the whole array puts the last k elements at the front
        (but in reversed order). Then reversing each half fixes the order.

    Time Complexity:  O(n)
    Space Complexity: O(1) -- truly in-place
    """
    n = len(nums)
    k = k % n  # Handle k > n

    if k == 0:
        return

    def reverse(start: int, end: int) -> None:
        """Reverse elements in nums[start:end+1] in-place."""
        while start < end:
            nums[start], nums[end] = nums[end], nums[start]
            start += 1
            end -= 1

    # Three reverses
    reverse(0, n - 1)       # Reverse entire array
    reverse(0, k - 1)       # Reverse first k elements
    reverse(k, n - 1)       # Reverse remaining n-k elements


# ============================================================================
# Approach 3: Cyclic Replacements
# ============================================================================
def rotate_cyclic(nums: List[int], k: int) -> None:
    """
    Rotate array using cyclic replacements.

    Strategy:
        - Start from index 0, move the element to its target position
          (current + k) % n.
        - The displaced element is then moved to ITS target position.
        - Continue until we return to the starting index (one cycle complete).
        - If not all elements are placed, start a new cycle from index + 1.
        - Total elements moved = n (we stop after moving n elements).

    Time Complexity:  O(n) -- each element is moved exactly once
    Space Complexity: O(1)
    """
    n = len(nums)
    k = k % n

    if k == 0:
        return

    count = 0           # Total elements placed in correct position
    start = 0           # Starting index of current cycle

    while count < n:
        current = start
        prev_val = nums[start]

        # Traverse the cycle
        while True:
            next_idx = (current + k) % n
            # Save the value at next_idx, then place prev_val there
            nums[next_idx], prev_val = prev_val, nums[next_idx]
            current = next_idx
            count += 1

            # If we've come back to start, this cycle is complete
            if current == start:
                break

        start += 1  # Start the next cycle


# ============================================================================
# Test Cases
# ============================================================================
if __name__ == "__main__":

    # --- Test Approach 1: Extra Array ---
    nums1 = [1, 2, 3, 4, 5, 6, 7]
    rotate_extra_array(nums1, 3)
    assert nums1 == [5, 6, 7, 1, 2, 3, 4], f"Test 1a failed: {nums1}"

    nums2 = [-1, -100, 3, 99]
    rotate_extra_array(nums2, 2)
    assert nums2 == [3, 99, -1, -100], f"Test 1b failed: {nums2}"

    nums3 = [1, 2]
    rotate_extra_array(nums3, 3)  # k > n
    assert nums3 == [2, 1], f"Test 1c failed: {nums3}"

    # --- Test Approach 2: Reverse ---
    nums4 = [1, 2, 3, 4, 5, 6, 7]
    rotate_reverse(nums4, 3)
    assert nums4 == [5, 6, 7, 1, 2, 3, 4], f"Test 2a failed: {nums4}"

    nums5 = [-1, -100, 3, 99]
    rotate_reverse(nums5, 2)
    assert nums5 == [3, 99, -1, -100], f"Test 2b failed: {nums5}"

    nums6 = [1, 2]
    rotate_reverse(nums6, 3)
    assert nums6 == [2, 1], f"Test 2c failed: {nums6}"

    # --- Test Approach 3: Cyclic Replacements ---
    nums7 = [1, 2, 3, 4, 5, 6, 7]
    rotate_cyclic(nums7, 3)
    assert nums7 == [5, 6, 7, 1, 2, 3, 4], f"Test 3a failed: {nums7}"

    nums8 = [-1, -100, 3, 99]
    rotate_cyclic(nums8, 2)
    assert nums8 == [3, 99, -1, -100], f"Test 3b failed: {nums8}"

    nums9 = [1, 2]
    rotate_cyclic(nums9, 3)
    assert nums9 == [2, 1], f"Test 3c failed: {nums9}"

    # --- Edge Cases ---
    nums10 = [1]
    rotate_reverse(nums10, 0)
    assert nums10 == [1], f"Test edge-1 failed: {nums10}"

    nums11 = [1, 2, 3]
    rotate_reverse(nums11, 6)  # k is a multiple of n
    assert nums11 == [1, 2, 3], f"Test edge-2 failed: {nums11}"

    nums12 = [1, 2, 3, 4, 5, 6]
    rotate_cyclic(nums12, 2)
    assert nums12 == [5, 6, 1, 2, 3, 4], f"Test edge-3 failed: {nums12}"

    print("All test cases passed!")
