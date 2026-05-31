"""
LeetCode 242 - Valid Anagram
============================

Problem:
    Given two strings `s` and `t`, return True if `t` is an anagram of `s`,
    and False otherwise.

    An anagram is a word or phrase formed by rearranging the letters of a
    different word or phrase, using all the original letters exactly once.

Examples:
    Input: s = "anagram", t = "nagaram"
    Output: True

    Input: s = "rat", t = "car"
    Output: False

Constraints:
    - 1 <= s.length, t.length <= 5 * 10^4
    - s and t consist of lowercase English letters.

Follow-up:
    What if the inputs contain Unicode characters?
    How would you adapt your solution to such a case?
"""

from collections import Counter


class Solution:
    # ------------------------------------------------------------------ #
    # Approach 1: Sorting
    # ------------------------------------------------------------------ #
    # If two strings are anagrams, sorting them will produce the same
    # result. We simply compare the sorted versions.
    #
    # Time Complexity : O(n log n)   -- dominated by sorting
    # Space Complexity: O(n)         -- sorted() creates a new list
    # ------------------------------------------------------------------ #
    def isAnagram_sorting(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        return sorted(s) == sorted(t)

    # ------------------------------------------------------------------ #
    # Approach 2: Counter / Hash Map (collections.Counter)
    # ------------------------------------------------------------------ #
    # Count the frequency of each character in both strings and compare.
    # Python's Counter makes this a one-liner.
    #
    # Time Complexity : O(n)   -- single pass to build each Counter
    # Space Complexity: O(1)   -- at most 26 lowercase English letters
    # ------------------------------------------------------------------ #
    def isAnagram_counter(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        return Counter(s) == Counter(t)

    # ------------------------------------------------------------------ #
    # Approach 3: Manual Character Counting with dict
    # ------------------------------------------------------------------ #
    # Build a frequency dictionary for `s`, then decrement counts for
    # each character in `t`. If all counts are zero at the end, the
    # strings are anagrams.
    #
    # Time Complexity : O(n)
    # Space Complexity: O(1)   -- at most 26 keys
    # ------------------------------------------------------------------ #
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False

        char_count = {}

        # Build frequency map from s
        for ch in s:
            char_count[ch] = char_count.get(ch, 0) + 1

        # Decrement counts using t
        for ch in t:
            if ch not in char_count or char_count[ch] == 0:
                return False
            char_count[ch] -= 1

        # All counts should be zero
        return all(v == 0 for v in char_count.values())


# ====================================================================== #
#                           TEST CASES                                    #
# ====================================================================== #
if __name__ == "__main__":
    sol = Solution()

    # --- Test all three approaches ---
    approaches = [
        ("Sorting", sol.isAnagram_sorting),
        ("Counter", sol.isAnagram_counter),
        ("Manual Dict", sol.isAnagram),
    ]

    for name, func in approaches:
        # Basic valid anagram
        assert func("anagram", "nagaram") is True, f"{name}: basic anagram failed"

        # Not an anagram
        assert func("rat", "car") is False, f"{name}: not anagram failed"

        # Different lengths
        assert func("a", "ab") is False, f"{name}: different lengths failed"
        assert func("abc", "ab") is False, f"{name}: different lengths (2) failed"

        # Empty strings (both empty  trivially anagrams)
        assert func("", "") is True, f"{name}: empty strings failed"

        # Single character -- same
        assert func("a", "a") is True, f"{name}: single char same failed"

        # Single character -- different
        assert func("a", "b") is False, f"{name}: single char different failed"

        # All same characters
        assert func("aaa", "aaa") is True, f"{name}: all same chars failed"

        # Same characters, different frequencies
        assert func("aaab", "aab") is False, f"{name}: diff freq failed"

        # Longer anagram
        assert func("listen", "silent") is True, f"{name}: listen/silent failed"

        # Repeated characters
        assert func("aabb", "abab") is True, f"{name}: repeated chars failed"
        assert func("aabb", "abba") is True, f"{name}: repeated chars (2) failed"

        # Same string
        assert func("hello", "hello") is True, f"{name}: same string failed"

        print(f"   {name}: All test cases passed!")

    print("\nAll test cases passed!")
