"""
LeetCode 70 -- Climbing Stairs

Problem:
    You are climbing a staircase. It takes `n` steps to reach the top.
    Each time you can either climb 1 or 2 steps.
    In how many distinct ways can you climb to the top?

Constraints:
    - 1 <= n <= 45

Examples:
    Input: n = 2    Output: 2  (1+1 or 2)
    Input: n = 3    Output: 3  (1+1+1, 1+2, 2+1)
    Input: n = 5    Output: 8

Approaches:
    1. Naive Recursion     -- O(2^n) time, O(n) space (call stack)
    2. Memoization         -- O(n) time, O(n) space
    3. Dynamic Programming -- O(n) time, O(n) space (can reduce to O(1))
    4. Fibonacci Formula   -- O(n) time, O(1) space
"""

from functools import lru_cache


# 
# Approach 1: Naive Recursion -- O(2^n) time
# 
def climb_stairs_recursive(n: int) -> int:
    """
    Count distinct ways to climb n stairs using recursion.

    At each step, we can take 1 or 2 steps. The total ways
    to reach step n = ways(n-1) + ways(n-2).

    WARNING: Exponential time -- only suitable for small n.
    """
    if n <= 2:
        return n
    return climb_stairs_recursive(n - 1) + climb_stairs_recursive(n - 2)


# 
# Approach 2: Memoization (Top-Down DP) -- O(n) time, O(n) space
# 
@lru_cache(maxsize=None)
def climb_stairs_memo(n: int) -> int:
    """
    Count distinct ways using memoization.

    Cache previously computed results to avoid redundant work.
    """
    if n <= 2:
        return n
    return climb_stairs_memo(n - 1) + climb_stairs_memo(n - 2)


# 
# Approach 3: Dynamic Programming (Bottom-Up) -- O(n) time, O(1) space
# 
def climb_stairs_dp(n: int) -> int:
    """
    Count distinct ways using bottom-up dynamic programming.

    Build the solution iteratively from base cases:
        dp[1] = 1, dp[2] = 2
        dp[i] = dp[i-1] + dp[i-2]

    Optimized to use only two variables instead of a full array.
    """
    if n <= 2:
        return n

    prev2, prev1 = 1, 2  # dp[1], dp[2]
    for _ in range(3, n + 1):
        current = prev1 + prev2
        prev2 = prev1
        prev1 = current

    return prev1


# 
# Approach 4: Fibonacci -- O(n) time, O(1) space
# 
def climb_stairs_fibonacci(n: int) -> int:
    """
    The climbing stairs problem is equivalent to finding the
    (n+1)th Fibonacci number.

    fib(1)=1, fib(2)=2, fib(k)=fib(k-1)+fib(k-2)
    """
    if n <= 2:
        return n

    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b

    return b


# 
# Test Cases
# 
if __name__ == "__main__":
    # Test all approaches
    test_cases = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 5),
        (5, 8),
        (10, 89),
        (20, 10946),
        (45, 1836311903),
    ]

    # Approach 1: Naive recursion (only small values due to O(2^n))
    for n, expected in test_cases[:5]:
        assert climb_stairs_recursive(n) == expected, \
            f"Recursive failed for n={n}"

    # Approach 2: Memoization
    for n, expected in test_cases:
        assert climb_stairs_memo(n) == expected, \
            f"Memoization failed for n={n}"

    # Approach 3: Dynamic Programming
    for n, expected in test_cases:
        assert climb_stairs_dp(n) == expected, \
            f"DP failed for n={n}"

    # Approach 4: Fibonacci
    for n, expected in test_cases:
        assert climb_stairs_fibonacci(n) == expected, \
            f"Fibonacci failed for n={n}"

    print("All test cases passed!")
