"""
LeetCode 347 -- Top K Frequent Elements
=========================================
Given an integer array nums and an integer k, return the k most frequent elements.

Example:
    Input:  nums = [1,1,1,2,2,3], k = 2
    Output: [1,2]

Approaches: Counter, heapq, bucket sort.
"""

from collections import Counter
import heapq


def top_k_frequent_counter(nums, k):
    """
    Approach 1: Counter.most_common()
    Time: O(n log n), Space: O(n)
    """
    return [num for num, _ in Counter(nums).most_common(k)]


def top_k_frequent_heap(nums, k):
    """
    Approach 2: Min-heap of size k.
    Time: O(n log k), Space: O(n)
    """
    count = Counter(nums)
    return heapq.nlargest(k, count.keys(), key=count.get)


def top_k_frequent_bucket(nums, k):
    """
    Approach 3: Bucket sort -- O(n) time!
    Create buckets where index = frequency.
    """
    count = Counter(nums)

    # Bucket: index = frequency, value = list of numbers with that frequency
    buckets = [[] for _ in range(len(nums) + 1)]
    for num, freq in count.items():
        buckets[freq].append(num)

    # Collect from highest frequency bucket
    result = []
    for freq in range(len(buckets) - 1, 0, -1):
        for num in buckets[freq]:
            result.append(num)
            if len(result) == k:
                return result

    return result


# ============================================================
# TESTS
# ============================================================

if __name__ == "__main__":
    for func in [top_k_frequent_counter, top_k_frequent_heap, top_k_frequent_bucket]:
        result = func([1, 1, 1, 2, 2, 3], 2)
        assert set(result) == {1, 2}, f"Test 1 failed: {result}"

        result = func([1], 1)
        assert result == [1], f"Test 2 failed: {result}"

        result = func([4, 4, 4, 1, 1, 2, 2, 2, 3], 2)
        assert set(result) == {4, 2}, f"Test 3 failed: {result}"

    print("All test cases passed")
