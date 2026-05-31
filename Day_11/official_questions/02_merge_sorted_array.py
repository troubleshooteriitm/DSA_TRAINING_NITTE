"""
LeetCode 88 -- Merge Sorted Array
==================================
Given two sorted arrays nums1 and nums2, merge nums2 into nums1 in-place.
nums1 has enough space (size m + n) to hold additional elements from nums2.

Example:
    Input:  nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3
    Output: [1,2,2,3,5,6]

Approach: Two pointers from the end.
Time: O(m + n), Space: O(1)
"""


def merge(nums1, m, nums2, n):
    """Merge nums2 into nums1 using two pointers from the end."""
    # Start from the end of both arrays
    i = m - 1      # Last element in nums1's actual data
    j = n - 1      # Last element in nums2
    k = m + n - 1  # Last position in nums1

    while i >= 0 and j >= 0:
        if nums1[i] > nums2[j]:
            nums1[k] = nums1[i]
            i -= 1
        else:
            nums1[k] = nums2[j]
            j -= 1
        k -= 1

    # If nums2 has remaining elements
    while j >= 0:
        nums1[k] = nums2[j]
        j -= 1
        k -= 1

    # No need to handle remaining nums1 -- they're already in place


# ============================================================
# TESTS
# ============================================================

if __name__ == "__main__":
    # Test 1
    nums1 = [1, 2, 3, 0, 0, 0]
    merge(nums1, 3, [2, 5, 6], 3)
    assert nums1 == [1, 2, 2, 3, 5, 6], f"Test 1 failed: {nums1}"

    # Test 2: nums1 empty
    nums1 = [0]
    merge(nums1, 0, [1], 1)
    assert nums1 == [1], f"Test 2 failed: {nums1}"

    # Test 3: nums2 empty
    nums1 = [1]
    merge(nums1, 1, [], 0)
    assert nums1 == [1], f"Test 3 failed: {nums1}"

    # Test 4: nums2 all smaller
    nums1 = [4, 5, 6, 0, 0, 0]
    merge(nums1, 3, [1, 2, 3], 3)
    assert nums1 == [1, 2, 3, 4, 5, 6], f"Test 4 failed: {nums1}"

    # Test 5: interleaved
    nums1 = [1, 3, 5, 0, 0, 0]
    merge(nums1, 3, [2, 4, 6], 3)
    assert nums1 == [1, 2, 3, 4, 5, 6], f"Test 5 failed: {nums1}"

    print("All test cases passed")
