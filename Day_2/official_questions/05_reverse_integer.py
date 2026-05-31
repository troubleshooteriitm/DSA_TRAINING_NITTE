"""
LeetCode 7 - Reverse Integer
==============================

Problem:
    Given a signed 32-bit integer `x`, return `x` with its digits reversed.
    If reversing `x` causes the value to go outside the signed 32-bit
    integer range [-2^31, 2^31 - 1], then return 0.

    Assume the environment does not allow you to store 64-bit integers
    (signed or unsigned).

Examples:
    Input: x = 123
    Output: 321

    Input: x = -123
    Output: -321

    Input: x = 120
    Output: 21   (trailing zeros are dropped)

    Input: x = 0
    Output: 0

Constraints:
    - -2^31 <= x <= 2^31 - 1

32-bit signed integer range:
    - Minimum: -2,147,483,648  (-2^31)
    - Maximum:  2,147,483,647  (2^31 - 1)
"""


class Solution:
    # ------------------------------------------------------------------ #
    # Approach: Mathematical digit-by-digit reversal
    # ------------------------------------------------------------------ #
    # Extract digits from the end using modulo and division, then build
    # the reversed number. Check for overflow before each multiplication.
    #
    # Key details:
    #   - Handle negative numbers by tracking the sign separately.
    #   - Trailing zeros in the input (e.g., 120) naturally disappear
    #     because leading zeros in the reversed number are not stored.
    #   - Overflow check: before doing result = result * 10 + digit,
    #     verify that result won't exceed INT_MAX // 10.
    #
    # Time Complexity : O(log(x))  -- number of digits
    # Space Complexity: O(1)
    # ------------------------------------------------------------------ #

    INT_MIN = -(2 ** 31)        # -2,147,483,648
    INT_MAX = 2 ** 31 - 1      #  2,147,483,647

    def reverse(self, x: int) -> int:
        # Determine sign and work with absolute value
        sign = -1 if x < 0 else 1
        x = abs(x)

        result = 0
        while x != 0:
            digit = x % 10
            x //= 10

            # Overflow check before multiplying
            # If result > INT_MAX // 10, then result * 10 will overflow.
            # If result == INT_MAX // 10, then adding digit > 7 overflows
            # (since INT_MAX ends in 7: 2,147,483,647).
            if result > self.INT_MAX // 10:
                return 0
            if result == self.INT_MAX // 10 and digit > 7:
                return 0

            result = result * 10 + digit

        result *= sign

        # Final bounds check (covers negative overflow edge case)
        if result < self.INT_MIN or result > self.INT_MAX:
            return 0

        return result

    # ------------------------------------------------------------------ #
    # Alternative: String-based reversal (simpler but uses extra space)
    # ------------------------------------------------------------------ #
    def reverse_string(self, x: int) -> int:
        sign = -1 if x < 0 else 1
        reversed_str = str(abs(x))[::-1]
        result = sign * int(reversed_str)

        # Check 32-bit overflow
        if result < self.INT_MIN or result > self.INT_MAX:
            return 0
        return result


# ====================================================================== #
#                           TEST CASES                                    #
# ====================================================================== #
if __name__ == "__main__":
    sol = Solution()

    approaches = [
        ("Mathematical", sol.reverse),
        ("String-based", sol.reverse_string),
    ]

    for name, func in approaches:
        # Positive number
        assert func(123) == 321, f"{name}: positive failed"

        # Negative number
        assert func(-123) == -321, f"{name}: negative failed"

        # Trailing zeros (120  21)
        assert func(120) == 21, f"{name}: trailing zeros failed"

        # Zero
        assert func(0) == 0, f"{name}: zero failed"

        # Single digit
        assert func(5) == 5, f"{name}: single digit failed"
        assert func(-8) == -8, f"{name}: single negative digit failed"

        # Positive overflow (1534236469 reversed = 9646324351 > INT_MAX)
        assert func(1534236469) == 0, f"{name}: positive overflow failed"

        # Negative overflow (-1534236469 reversed = -9646324351 < INT_MIN)
        assert func(-1534236469) == 0, f"{name}: negative overflow failed"

        # Edge: INT_MAX and INT_MIN boundaries
        # 2147483647 reversed = 7463847412 > INT_MAX  0
        assert func(2147483647) == 0, f"{name}: INT_MAX overflow failed"

        # -2147483648 reversed = -8463847412 < INT_MIN  0
        assert func(-2147483648) == 0, f"{name}: INT_MIN overflow failed"

        # Number that reverses within bounds
        assert func(1463847412) == 2147483641, f"{name}: large valid reverse failed"

        # Trailing zeros with negative
        assert func(-120) == -21, f"{name}: negative trailing zeros failed"

        # All same digits
        assert func(1111) == 1111, f"{name}: all same digits failed"

        # 10, 100, 1000 -- edge cases with trailing zeros
        assert func(10) == 1, f"{name}: 10 failed"
        assert func(100) == 1, f"{name}: 100 failed"
        assert func(1000) == 1, f"{name}: 1000 failed"

        print(f"   {name}: All test cases passed!")

    print("\nAll test cases passed!")
