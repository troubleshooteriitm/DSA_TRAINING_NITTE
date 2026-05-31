"""
LeetCode 219 -- Contains Duplicate II
======================================
Difficulty: Easy
URL: https://leetcode.com/problems/contains-duplicate-ii/

Problem Description:
    Given an integer array nums and an integer k, return true if there are
    two distinct indices i and j in the array such that:
        - nums[i] == nums[j]
        - abs(i - j) <= k

    In other words, check if there is a duplicate element within a window
    of size k.

Approach -- Sliding Window with Set:
    Maintain a set that holds at most k elements representing the current
    sliding window. As we iterate through the array:

    1. If the current element is already in the set, we found a duplicate
       within distance k  return True.
    2. Add the current element to the set.
    3. If the set size exceeds k, remove the element that has left the
       window (the element at index i - k).

    This ensures we only compare elements within distance k of each other.

Alternative Approach -- Hash Map:
    Use a dictionary to store the last seen index of each element.
    If we encounter an element whose last index is within k distance,
    return True.

Time Complexity: O(n) -- single pass through the array
Space Complexity: O(min(n, k)) -- the set holds at most k+1 elements
"""


def contains_nearby_duplicate(nums: list, k: int) -> bool:
    """
    Check if there are duplicate elements within distance k.

    Uses a sliding window approach with a set to maintain the
    current window of elements. The window size is at most k.

    Args:
        nums: List of integers to check.
        k: Maximum allowed distance between duplicate elements.

    Returns:
        True if duplicate elements exist within distance k, False otherwise.
    """
    # Set to track elements in the current window of size k
    window = set()

    for i, num in enumerate(nums):
        # If current number is already in the window, duplicate found!
        if num in window:
            return True

        # Add current number to the window
        window.add(num)

        # If window size exceeds k, remove the oldest element
        # The oldest element is nums[i - k] (it's now outside the window)
        if len(window) > k:
            window.remove(nums[i - k])

    return False


def contains_nearby_duplicate_hashmap(nums: list, k: int) -> bool:
    """
    Alternative approach using a hash map to track last seen index.

    For each element, we store its most recent index. If we encounter
    the element again and the difference in indices is <= k, we return True.

    Args:
        nums: List of integers to check.
        k: Maximum allowed distance between duplicate elements.

    Returns:
        True if duplicate elements exist within distance k, False otherwise.
    """
    # Dictionary mapping element  most recent index
    last_seen = {}

    for i, num in enumerate(nums):
        if num in last_seen and i - last_seen[num] <= k:
            return True
        last_seen[num] = i

    return False


# ============================================================
# Test Cases
# ============================================================

if __name__ == '__main__':

    # Test 1: LeetCode Example 1 -- duplicate within distance k
    # nums[0] = 1 and nums[3] = 1, abs(0-3) = 3 <= 3
    assert contains_nearby_duplicate([1, 2, 3, 1], 3) is True

    # Test 2: LeetCode Example 2 -- duplicate within distance k
    # nums[0] = 1 and nums[1] = 1 (NOT the one at index 3), abs(0-1) = 1 <= 1
    assert contains_nearby_duplicate([1, 0, 1, 1], 1) is True

    # Test 3: LeetCode Example 3 -- duplicate exists but too far apart
    # nums[0] = 1 and nums[3] = 1, abs(0-3) = 3 > 2
    assert contains_nearby_duplicate([1, 2, 3, 1, 2, 3], 2) is False

    # Test 4: No duplicates at all
    assert contains_nearby_duplicate([1, 2, 3, 4, 5], 3) is False

    # Test 5: Adjacent duplicates (k=1)
    assert contains_nearby_duplicate([1, 1], 1) is True

    # Test 6: Empty array
    assert contains_nearby_duplicate([], 1) is False

    # Test 7: Single element
    assert contains_nearby_duplicate([1], 1) is False

    # Test 8: k=0, duplicates must be at same index (impossible)
    assert contains_nearby_duplicate([1, 2, 1], 0) is False

    # Test 9: All same elements
    assert contains_nearby_duplicate([1, 1, 1, 1], 2) is True

    # Test 10: Large k value
    assert contains_nearby_duplicate([1, 2, 3, 4, 1], 10) is True

    # --- Verify hash map approach gives same results ---
    assert contains_nearby_duplicate_hashmap([1, 2, 3, 1], 3) is True
    assert contains_nearby_duplicate_hashmap([1, 0, 1, 1], 1) is True
    assert contains_nearby_duplicate_hashmap([1, 2, 3, 1, 2, 3], 2) is False
    assert contains_nearby_duplicate_hashmap([1, 2, 3, 4, 5], 3) is False
    assert contains_nearby_duplicate_hashmap([], 1) is False

    print("All test cases passed!")
