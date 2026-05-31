"""
Sliding Window Pattern -- Practice Examples
============================================
This module demonstrates three key sliding window patterns:

1. Fixed-Size Window -- Maximum sum subarray of size k
2. Variable-Size Window -- Longest substring without repeating characters
3. Minimum Window Substring -- Smallest window containing all target chars

The sliding window technique converts brute-force O(n*k) or O(n²)
solutions into efficient O(n) solutions by maintaining a "window"
that slides across the data.
"""

from collections import Counter


# ============================================================
# 1. FIXED-SIZE SLIDING WINDOW
# ============================================================

def max_sum_subarray_of_size_k(nums: list, k: int) -> int:
    """
    Find the maximum sum of any contiguous subarray of size k.

    Pattern: Fixed-Size Sliding Window
    - Initialize window with first k elements
    - Slide by adding right element and removing left element
    - Track maximum sum seen

    Args:
        nums: List of integers.
        k: Size of the sliding window.

    Returns:
        Maximum sum of any subarray of size k.
        Returns 0 if array has fewer than k elements.

    Time Complexity: O(n) -- single pass
    Space Complexity: O(1) -- only tracking sums

    Example:
        nums = [2, 1, 5, 1, 3, 2], k = 3
        Windows: [2,1,5]=8, [1,5,1]=7, [5,1,3]=9, [1,3,2]=6
        Answer: 9
    """
    if not nums or len(nums) < k:
        return 0

    # Step 1: Calculate sum of the first window
    window_sum = sum(nums[:k])
    max_sum = window_sum

    # Step 2: Slide the window from left to right
    for i in range(k, len(nums)):
        # Add the new element entering the window (right side)
        # Remove the element leaving the window (left side)
        window_sum += nums[i] - nums[i - k]

        # Update maximum
        max_sum = max(max_sum, window_sum)

    return max_sum


def find_all_averages_of_size_k(nums: list, k: int) -> list:
    """
    Find the average of each contiguous subarray of size k.

    Another fixed-size window example.

    Args:
        nums: List of numbers.
        k: Window size.

    Returns:
        List of averages for each window position.
    """
    if not nums or len(nums) < k:
        return []

    result = []
    window_sum = sum(nums[:k])
    result.append(window_sum / k)

    for i in range(k, len(nums)):
        window_sum += nums[i] - nums[i - k]
        result.append(window_sum / k)

    return result


# ============================================================
# 2. VARIABLE-SIZE SLIDING WINDOW
# ============================================================

def longest_substring_without_repeat(s: str) -> int:
    """
    Find the length of the longest substring without repeating characters.

    Pattern: Variable-Size Sliding Window
    - Expand window by moving right pointer
    - When a duplicate is found, shrink window from the left
    - Track maximum window size

    Args:
        s: Input string.

    Returns:
        Length of the longest substring without repeating characters.

    Time Complexity: O(n) -- each character is visited at most twice
    Space Complexity: O(min(m, n)) -- m is charset size, n is string length

    Example:
        s = "abcabcbb"
        Substrings: "abc" (len 3), "bca" (len 3), "cab" (len 3)
        Answer: 3
    """
    # Set to track characters in the current window
    char_set = set()
    left = 0
    max_length = 0

    for right in range(len(s)):
        # If character is already in window, shrink from left
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1

        # Add current character to window
        char_set.add(s[right])

        # Update maximum length
        max_length = max(max_length, right - left + 1)

    return max_length


def longest_substring_with_k_distinct(s: str, k: int) -> int:
    """
    Find the length of the longest substring with at most k distinct characters.

    Another variable-size window problem.

    Args:
        s: Input string.
        k: Maximum number of distinct characters allowed.

    Returns:
        Length of the longest valid substring.

    Time Complexity: O(n)
    Space Complexity: O(k)
    """
    if not s or k == 0:
        return 0

    char_count = {}
    left = 0
    max_length = 0

    for right in range(len(s)):
        # Add right character to window
        char_count[s[right]] = char_count.get(s[right], 0) + 1

        # Shrink window while we have more than k distinct characters
        while len(char_count) > k:
            char_count[s[left]] -= 1
            if char_count[s[left]] == 0:
                del char_count[s[left]]
            left += 1

        # Update maximum length
        max_length = max(max_length, right - left + 1)

    return max_length


# ============================================================
# 3. MINIMUM WINDOW SUBSTRING
# ============================================================

def minimum_window_substring(s: str, t: str) -> str:
    """
    Find the minimum window in s which contains all characters of t.

    Pattern: Variable-Size Sliding Window with Character Counting
    - Use Counter to track required characters
    - Expand window until all characters are found
    - Then shrink from left to minimize window size
    - Track the smallest valid window

    This is a classic hard problem (LeetCode 76) that combines
    sliding window with hash map counting.

    Args:
        s: Source string to search in.
        t: Target string containing required characters.

    Returns:
        The minimum window substring, or "" if no valid window exists.

    Time Complexity: O(|s| + |t|) -- each character visited at most twice
    Space Complexity: O(|s| + |t|) -- for the counters

    Example:
        s = "ADOBECODEBANC", t = "ABC"
        Answer: "BANC" (contains A, B, C with minimum length)
    """
    if not s or not t or len(s) < len(t):
        return ""

    # Count of characters we need
    need = Counter(t)
    # Number of unique characters we still need to find
    required = len(need)

    # Current window character counts
    window_counts = {}
    # Number of unique characters in current window with sufficient count
    formed = 0

    # Track the best (smallest) window: (window_length, left, right)
    best = (float('inf'), 0, 0)

    left = 0

    for right in range(len(s)):
        # Add character from the right to the window
        char = s[right]
        window_counts[char] = window_counts.get(char, 0) + 1

        # Check if current character's count matches what we need
        if char in need and window_counts[char] == need[char]:
            formed += 1

        # Try to shrink the window from the left
        while formed == required:
            # Update best window if current is smaller
            window_length = right - left + 1
            if window_length < best[0]:
                best = (window_length, left, right)

            # Remove leftmost character from window
            left_char = s[left]
            window_counts[left_char] -= 1
            if left_char in need and window_counts[left_char] < need[left_char]:
                formed -= 1

            left += 1

    # Return the best window, or "" if none found
    length, start, end = best
    return s[start:end + 1] if length != float('inf') else ""


# ============================================================
# Test Cases
# ============================================================

if __name__ == '__main__':

    # --- Test 1: Max Sum Subarray of Size K ---
    assert max_sum_subarray_of_size_k([2, 1, 5, 1, 3, 2], 3) == 9
    assert max_sum_subarray_of_size_k([2, 3, 4, 1, 5], 2) == 7
    assert max_sum_subarray_of_size_k([1, 1, 1, 1, 1], 3) == 3
    assert max_sum_subarray_of_size_k([5], 1) == 5
    assert max_sum_subarray_of_size_k([], 3) == 0
    assert max_sum_subarray_of_size_k([1, 2], 3) == 0  # Array too short
    print(" max_sum_subarray_of_size_k -- all tests passed")

    # --- Test 2: Find All Averages of Size K ---
    result = find_all_averages_of_size_k([1, 3, 2, 6, -1, 4, 1, 8, 2], 5)
    expected = [2.2, 2.8, 2.4, 3.6, 2.8]
    assert len(result) == len(expected)
    for r, e in zip(result, expected):
        assert abs(r - e) < 1e-9, f"Expected {e}, got {r}"
    print(" find_all_averages_of_size_k -- all tests passed")

    # --- Test 3: Longest Substring Without Repeat ---
    assert longest_substring_without_repeat("abcabcbb") == 3
    assert longest_substring_without_repeat("bbbbb") == 1
    assert longest_substring_without_repeat("pwwkew") == 3
    assert longest_substring_without_repeat("") == 0
    assert longest_substring_without_repeat("abcdef") == 6
    assert longest_substring_without_repeat("aab") == 2
    print(" longest_substring_without_repeat -- all tests passed")

    # --- Test 4: Longest Substring with K Distinct ---
    assert longest_substring_with_k_distinct("araaci", 2) == 4   # "araa"
    assert longest_substring_with_k_distinct("araaci", 1) == 2   # "aa"
    assert longest_substring_with_k_distinct("cbbebi", 3) == 5   # "cbbeb"
    assert longest_substring_with_k_distinct("", 2) == 0
    assert longest_substring_with_k_distinct("abc", 0) == 0
    print(" longest_substring_with_k_distinct -- all tests passed")

    # --- Test 5: Minimum Window Substring ---
    assert minimum_window_substring("ADOBECODEBANC", "ABC") == "BANC"
    assert minimum_window_substring("a", "a") == "a"
    assert minimum_window_substring("a", "aa") == ""
    assert minimum_window_substring("ab", "b") == "b"
    assert minimum_window_substring("", "ABC") == ""
    assert minimum_window_substring("ABC", "") == ""
    print(" minimum_window_substring -- all tests passed")

    print("\nAll test cases passed!")
