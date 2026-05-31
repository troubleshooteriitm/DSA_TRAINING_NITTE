"""
LeetCode 1 -- Two Sum

Problem:
    Given an array of integers `nums` and an integer `target`,
    return the indices of the two numbers such that they add up to `target`.

    You may assume that each input would have exactly one solution,
    and you may not use the same element twice.

    You can return the answer in any order.

Constraints:
    - 2 <= nums.length <= 10^4
    - -10^9 <= nums[i] <= 10^9
    - -10^9 <= target <= 10^9
    - Only one valid answer exists.

Examples:
    Input: nums = [2,7,11,15], target = 9    Output: [0,1]
    Input: nums = [3,2,4], target = 6        Output: [1,2]
    Input: nums = [3,3], target = 6          Output: [0,1]

Approaches:
    1. Brute Force  -- O(n²) time, O(1) space
    2. Hash Map     -- O(n) time, O(n) space
"""

from typing import List


# 
# Approach 1: Brute Force -- O(n²) time, O(1) space
# 
def two_sum_brute(nums: List[int], target: int) -> List[int]:
    """
    Check every pair of numbers to find the two that add up to target.

    For each element, iterate through the rest of the array to find
    a complement (target - nums[i]).

    Time:  O(n²) -- nested loops
    Space: O(1)  -- no extra data structures
    """
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []  # No solution found (shouldn't happen per constraints)


# 
# Approach 2: Hash Map (Optimal) -- O(n) time, O(n) space
# 
def two_sum_hashmap(nums: List[int], target: int) -> List[int]:
    """
    Use a hash map to store each number's index as we iterate.

    For each number, check if its complement (target - num) has
    already been seen. If yes, return both indices.

    Time:  O(n) -- single pass through the array
    Space: O(n) -- hash map stores up to n elements
    """
    seen = {}  # value -> index

    for i, num in enumerate(nums):
        complement = target - num

        if complement in seen:
            return [seen[complement], i]

        seen[num] = i

    return []  # No solution found


# 
# Test Cases
# 
if __name__ == "__main__":
    #  Test Case 1: Basic case 
    nums1, target1 = [2, 7, 11, 15], 9
    assert two_sum_brute(nums1, target1) == [0, 1], \
        f"Brute force failed for test 1"
    assert two_sum_hashmap(nums1, target1) == [0, 1], \
        f"Hash map failed for test 1"

    #  Test Case 2: Non-adjacent elements 
    nums2, target2 = [3, 2, 4], 6
    assert two_sum_brute(nums2, target2) == [1, 2], \
        f"Brute force failed for test 2"
    assert two_sum_hashmap(nums2, target2) == [1, 2], \
        f"Hash map failed for test 2"

    #  Test Case 3: Duplicate values 
    nums3, target3 = [3, 3], 6
    assert two_sum_brute(nums3, target3) == [0, 1], \
        f"Brute force failed for test 3"
    assert two_sum_hashmap(nums3, target3) == [0, 1], \
        f"Hash map failed for test 3"

    #  Test Case 4: Negative numbers 
    nums4, target4 = [-1, -2, -3, -4, -5], -8
    assert two_sum_brute(nums4, target4) == [2, 4], \
        f"Brute force failed for test 4"
    assert two_sum_hashmap(nums4, target4) == [2, 4], \
        f"Hash map failed for test 4"

    #  Test Case 5: Mixed positive and negative 
    nums5, target5 = [1, -3, 4, 2, -1], 1
    result_brute = two_sum_brute(nums5, target5)
    result_hash = two_sum_hashmap(nums5, target5)
    assert nums5[result_brute[0]] + nums5[result_brute[1]] == target5, \
        f"Brute force failed for test 5"
    assert nums5[result_hash[0]] + nums5[result_hash[1]] == target5, \
        f"Hash map failed for test 5"

    #  Test Case 6: Larger array 
    nums6 = list(range(1, 101))  # [1, 2, ..., 100]
    target6 = 199  # 99 + 100
    assert two_sum_brute(nums6, target6) == [98, 99], \
        f"Brute force failed for test 6"
    assert two_sum_hashmap(nums6, target6) == [98, 99], \
        f"Hash map failed for test 6"

    print("All test cases passed!")
