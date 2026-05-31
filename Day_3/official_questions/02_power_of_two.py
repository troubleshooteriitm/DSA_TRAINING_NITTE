"""
LeetCode 231 -- Power of Two
============================

Problem:
    Given an integer n, return True if it is a power of two. Otherwise,
    return False.

    An integer n is a power of two if there exists an integer x such that
    n == 2^x.

Examples:
    Input: n = 1    -> Output: True   (2^0 = 1)
    Input: n = 16   -> Output: True   (2^4 = 16)
    Input: n = 3    -> Output: False
    Input: n = 0    -> Output: False
    Input: n = -4   -> Output: False

Constraints:
    -2^31 <= n <= 2^31 - 1

Follow-up:
    Could you solve it without loops/recursion?
"""

import math


class Solution:
    # -------------------------------------------------------------------------
    # Approach 1: Iterative -- Repeatedly Divide by 2
    # -------------------------------------------------------------------------
    def isPowerOfTwo_iterative(self, n: int) -> bool:
        """
        Keep dividing n by 2 as long as it's even. If we end up with 1,
        the original number was a power of two.

        Time Complexity : O(log n)
        Space Complexity: O(1)
        """
        if n <= 0:
            return False

        while n > 1:
            if n % 2 != 0:
                return False
            n //= 2

        return True  # n is now 1

    # -------------------------------------------------------------------------
    # Approach 2: Bit Manipulation -- n & (n - 1) == 0
    # -------------------------------------------------------------------------
    def isPowerOfTwo_bit(self, n: int) -> bool:
        """
        Key Insight: A power of two in binary has exactly one '1' bit.
            e.g., 8  = 1000
                  7  = 0111
                  8 & 7 = 0000 

        If n is a power of two, then n & (n - 1) == 0.

        Time Complexity : O(1)
        Space Complexity: O(1)
        """
        return n > 0 and (n & (n - 1)) == 0

    # -------------------------------------------------------------------------
    # Approach 3: Math -- Logarithm Base 2
    # -------------------------------------------------------------------------
    def isPowerOfTwo_log(self, n: int) -> bool:
        """
        If n is a power of 2, then log2(n) should be an integer.

        We use math.log2 and check if the result is a whole number.
        Note: Floating-point precision can be tricky, so we round and verify.

        Time Complexity : O(1)
        Space Complexity: O(1)
        """
        if n <= 0:
            return False

        log_val = math.log2(n)
        return log_val == int(log_val)


# =============================================================================
# Test Cases
# =============================================================================
if __name__ == "__main__":
    sol = Solution()

    # ---------- Test data ----------
    test_cases = [
        # (input, expected)
        (1, True),       # 2^0
        (2, True),       # 2^1
        (4, True),       # 2^2
        (8, True),       # 2^3
        (16, True),      # 2^4
        (32, True),      # 2^5
        (64, True),      # 2^6
        (1024, True),    # 2^10
        (1048576, True), # 2^20
        (3, False),
        (5, False),
        (6, False),
        (10, False),
        (0, False),      # Edge case: zero
        (-1, False),     # Edge case: negative
        (-4, False),     # Edge case: negative power of two
        (-16, False),    # Edge case: negative
        (7, False),
        (100, False),
    ]

    # ---------- Verify all three approaches ----------
    for n, expected in test_cases:
        r1 = sol.isPowerOfTwo_iterative(n)
        r2 = sol.isPowerOfTwo_bit(n)
        r3 = sol.isPowerOfTwo_log(n)

        assert r1 == expected, (
            f"Iterative FAILED for n={n}: got {r1}, expected {expected}"
        )
        assert r2 == expected, (
            f"Bit manipulation FAILED for n={n}: got {r2}, expected {expected}"
        )
        assert r3 == expected, (
            f"Log FAILED for n={n}: got {r3}, expected {expected}"
        )

    # ---------- Large power of two ----------
    large_power = 2 ** 30  # 1,073,741,824
    assert sol.isPowerOfTwo_iterative(large_power) is True
    assert sol.isPowerOfTwo_bit(large_power) is True
    assert sol.isPowerOfTwo_log(large_power) is True

    # Non-power near a large power
    assert sol.isPowerOfTwo_iterative(large_power + 1) is False
    assert sol.isPowerOfTwo_bit(large_power + 1) is False
    assert sol.isPowerOfTwo_log(large_power + 1) is False

    print("All test cases passed!")
