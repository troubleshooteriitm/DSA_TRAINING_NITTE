"""
LeetCode 169 -- Majority Element

Problem:
    Given an array `nums` of size n, return the majority element.

    The majority element is the element that appears more than n / 2 times.
    You may assume that the majority element always exists in the array.

    Example 1:
        Input:  nums = [3, 2, 3]
        Output: 3

    Example 2:
        Input:  nums = [2, 2, 1, 1, 1, 2, 2]
        Output: 2

    Constraints:
        - n == nums.length
        - 1 <= n <= 5 * 10^4
        - -10^9 <= nums[i] <= 10^9

    Follow up: Could you solve the problem in linear time and in O(1) space?

Approaches:
    1. Hash Map Counting          -- O(n) time, O(n) space
    2. Sorting                    -- O(n log n) time, O(1) space
    3. Boyer-Moore Voting Algo    -- O(n) time, O(1) space   Optimal
"""

from typing import List
from collections import Counter


# ============================================================================
# Approach 1: Hash Map Counting
# ============================================================================
def majority_element_hashmap(nums: List[int]) -> int:
    """
    Find the majority element using a frequency counter.

    Strategy:
        - Count occurrences of each element using a hash map.
        - Return the element whose count exceeds n // 2.

    Time Complexity:  O(n)
    Space Complexity: O(n)
    """
    counts = Counter(nums)
    threshold = len(nums) // 2

    for num, count in counts.items():
        if count > threshold:
            return num

    # Problem guarantees a majority element exists, so we never reach here
    return -1  # pragma: no cover


# ============================================================================
# Approach 2: Sorting
# ============================================================================
def majority_element_sorting(nums: List[int]) -> int:
    """
    Find the majority element using sorting.

    Strategy:
        - Sort the array.
        - Since the majority element appears more than n/2 times,
          it MUST occupy the middle position after sorting.

    Proof:
        If an element appears > n/2 times, no matter where it starts
        in the sorted array, it will always stretch across index n//2.

        Example: [1, 2, 2, 2, 3]  majority is 2, and nums[2] = 2 
        Example: [2, 2, 2, 3, 3]  majority is 2, and nums[2] = 2 

    Time Complexity:  O(n log n)
    Space Complexity: O(1) if sorting in-place, O(n) otherwise
    """
    nums_sorted = sorted(nums)
    return nums_sorted[len(nums) // 2]


# ============================================================================
# Approach 3: Boyer-Moore Voting Algorithm (Optimal)
# ============================================================================
def majority_element_boyer_moore(nums: List[int]) -> int:
    """
    Find the majority element using Boyer-Moore Voting Algorithm.

    Strategy:
        Maintain a 'candidate' and a 'count':

        1. Start with count = 0 and no candidate.
        2. For each element:
           - If count == 0, set current element as the new candidate.
           - If current element == candidate, increment count.
           - If current element != candidate, decrement count.
        3. The final candidate is the majority element.

    Intuition:
        Think of it as a "battle": the majority element has more than n/2
        soldiers. Even if every other element cancels one majority soldier,
        the majority element still has soldiers remaining at the end.

    Walkthrough with [2, 2, 1, 1, 1, 2, 2]:
        
         Step   Element    Count  Candidate                     
        
           1        2        1    2 (count was 0, new candidate)
           2        2        2    2 (match, count++)            
           3        1        1    2 (no match, count--)         
           4        1        0    2 (no match, count--)         
           5        1        1    1 (count was 0, new candidate)
           6        2        0    1 (no match, count--)         
           7        2        1    2 (count was 0, new candidate)
        
        Final candidate = 2 

    Time Complexity:  O(n) -- single pass through the array
    Space Complexity: O(1) -- only two variables used
    """
    candidate = None
    count = 0

    for num in nums:
        # When count drops to 0, pick a new candidate
        if count == 0:
            candidate = num
            count = 1
        elif num == candidate:
            count += 1
        else:
            count -= 1

    return candidate


# ============================================================================
# Approach 3b: Boyer-Moore with Verification
# ============================================================================
def majority_element_verified(nums: List[int]) -> int:
    """
    Boyer-Moore with a verification pass.

    When the problem does NOT guarantee a majority element exists,
    we need a second pass to verify the candidate actually appears
    more than n/2 times.

    Time Complexity:  O(n) -- two passes
    Space Complexity: O(1)
    """
    # Phase 1: Find candidate
    candidate = None
    count = 0

    for num in nums:
        if count == 0:
            candidate = num
            count = 1
        elif num == candidate:
            count += 1
        else:
            count -= 1

    # Phase 2: Verify candidate
    actual_count = sum(1 for num in nums if num == candidate)
    if actual_count > len(nums) // 2:
        return candidate
    else:
        return -1  # No majority element exists


# ============================================================================
# Test Cases
# ============================================================================
if __name__ == "__main__":

    # --- Basic Tests ---
    assert majority_element_hashmap([3, 2, 3]) == 3
    assert majority_element_hashmap([2, 2, 1, 1, 1, 2, 2]) == 2

    assert majority_element_sorting([3, 2, 3]) == 3
    assert majority_element_sorting([2, 2, 1, 1, 1, 2, 2]) == 2

    assert majority_element_boyer_moore([3, 2, 3]) == 3
    assert majority_element_boyer_moore([2, 2, 1, 1, 1, 2, 2]) == 2

    # --- Edge Cases ---
    # Single element
    assert majority_element_boyer_moore([1]) == 1

    # All same elements
    assert majority_element_boyer_moore([5, 5, 5, 5]) == 5

    # Two elements
    assert majority_element_boyer_moore([1, 1]) == 1

    # Majority at the boundaries
    assert majority_element_boyer_moore([1, 1, 1, 2, 2]) == 1  # majority at front
    assert majority_element_boyer_moore([2, 2, 1, 1, 1]) == 1  # majority at back

    # Large majority
    assert majority_element_boyer_moore([3, 3, 3, 3, 1, 2, 4]) == 3

    # --- Verified version tests ---
    assert majority_element_verified([3, 2, 3]) == 3
    assert majority_element_verified([1, 2, 3]) == -1  # No majority

    # --- Cross-check all approaches give same result ---
    test_arrays = [
        [3, 2, 3],
        [2, 2, 1, 1, 1, 2, 2],
        [1],
        [6, 6, 6, 7, 7],
        [10, 10, 10, 10, 5, 5, 5],
    ]

    for arr in test_arrays:
        r1 = majority_element_hashmap(arr)
        r2 = majority_element_sorting(arr)
        r3 = majority_element_boyer_moore(arr)
        assert r1 == r2 == r3, (
            f"Mismatch for {arr}: hashmap={r1}, sorting={r2}, boyer_moore={r3}"
        )

    print("All test cases passed!")
