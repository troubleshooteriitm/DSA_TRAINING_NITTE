"""
LeetCode 3 -- Longest Substring Without Repeating Characters
==============================================================
Given a string s, find the length of the longest substring
without repeating characters.

Example:
    Input:  "abcabcbb"
    Output: 3  (The answer is "abc")

Approach: Sliding Window with set/dict.
Time: O(n), Space: O(min(m, n)) where m = charset size
"""


def length_of_longest_substring(s):
    """Sliding window with set."""
    char_set = set()
    left = 0
    max_len = 0

    for right in range(len(s)):
        # Shrink window until no duplicate
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1

        char_set.add(s[right])
        max_len = max(max_len, right - left + 1)

    return max_len


def length_of_longest_substring_v2(s):
    """
    Optimized: Use dict to store last index of each character.
    Jump left pointer directly instead of moving one-by-one.
    """
    last_seen = {}
    left = 0
    max_len = 0

    for right, char in enumerate(s):
        if char in last_seen and last_seen[char] >= left:
            left = last_seen[char] + 1

        last_seen[char] = right
        max_len = max(max_len, right - left + 1)

    return max_len


# ============================================================
# TESTS
# ============================================================

if __name__ == "__main__":
    for func in [length_of_longest_substring, length_of_longest_substring_v2]:
        assert func("abcabcbb") == 3
        assert func("bbbbb") == 1
        assert func("pwwkew") == 3
        assert func("") == 0
        assert func(" ") == 1
        assert func("au") == 2
        assert func("dvdf") == 3
        assert func("abcdef") == 6

    print("All test cases passed")
