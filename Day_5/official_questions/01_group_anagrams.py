"""
LeetCode 49 -- Group Anagrams
=============================
Given an array of strings, group the anagrams together.
You can return the answer in any order.

Example:
    Input:  ["eat","tea","tan","ate","nat","bat"]
    Output: [["bat"],["nat","tan"],["ate","eat","tea"]]

Approach: Use sorted string as dictionary key.
Time:  O(n * k log k) where k is max string length
Space: O(n * k)
"""

from collections import defaultdict


def group_anagrams(strs):
    """Group anagrams using sorted string as key."""
    groups = defaultdict(list)
    for s in strs:
        key = "".join(sorted(s))
        groups[key].append(s)
    return list(groups.values())


def group_anagrams_v2(strs):
    """
    Group anagrams using character count as key.
    Time: O(n * k) -- avoids sorting each string.
    """
    groups = defaultdict(list)
    for s in strs:
        count = [0] * 26
        for c in s:
            count[ord(c) - ord('a')] += 1
        groups[tuple(count)].append(s)
    return list(groups.values())


# ============================================================
# TESTS
# ============================================================

if __name__ == "__main__":
    # Test 1
    result = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    result_sorted = sorted([sorted(g) for g in result])
    expected = sorted([sorted(g) for g in [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]])
    assert result_sorted == expected, f"Test 1 failed: {result}"

    # Test 2: empty string
    result = group_anagrams([""])
    assert result == [[""]], f"Test 2 failed: {result}"

    # Test 3: single char
    result = group_anagrams(["a"])
    assert result == [["a"]], f"Test 3 failed: {result}"

    # Test v2
    result2 = group_anagrams_v2(["eat", "tea", "tan", "ate", "nat", "bat"])
    result2_sorted = sorted([sorted(g) for g in result2])
    assert result2_sorted == expected, f"V2 Test failed: {result2}"

    print("All test cases passed")
