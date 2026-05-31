"""
LeetCode 136 -- Single Number (Bit Manipulation Focus)
=======================================================
Every element appears twice except for one. Find that single one.

Example:
    Input:  [4,1,2,1,2]
    Output: 4

Key Insight (XOR properties):
    - a ^ a = 0  (same number cancels out)
    - a ^ 0 = a  (XOR with 0 is identity)
    - XOR is commutative and associative

So XOR-ing all numbers: pairs cancel  only unique remains.
Time: O(n), Space: O(1) -- OPTIMAL
"""


def single_number(nums):
    """XOR all numbers -- pairs cancel, unique survives."""
    result = 0
    for num in nums:
        result ^= num
    return result


def single_number_v2(nums):
    """Using reduce for a functional approach."""
    from functools import reduce
    from operator import xor
    return reduce(xor, nums)


# ============================================================
# BIT MANIPULATION EXPLAINED
# ============================================================
# Binary example:
#   4 = 100
#   1 = 001
#   2 = 010
#   1 = 001
#   2 = 010
#
# XOR chain: 100 ^ 001 ^ 010 ^ 001 ^ 010
#          = 100 ^ (001 ^ 001) ^ (010 ^ 010)
#          = 100 ^ 000 ^ 000
#          = 100
#          = 4  


if __name__ == "__main__":
    for func in [single_number, single_number_v2]:
        assert func([2, 2, 1]) == 1
        assert func([4, 1, 2, 1, 2]) == 4
        assert func([1]) == 1
        assert func([0, 1, 0]) == 1
        assert func([99]) == 99

    print("All test cases passed")
