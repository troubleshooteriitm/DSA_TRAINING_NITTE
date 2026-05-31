"""
LeetCode 9 -- Palindrome Number
https://leetcode.com/problems/palindrome-number/

Difficulty: Easy

Problem:
    Given an integer x, return True if x is a palindrome integer,
    and False otherwise.

    An integer is a palindrome when it reads the same forward and
    backward. For example, 121 is a palindrome while 123 is not.

Constraints:
    -2^31 <= x <= 2^31 - 1

Examples:
    Input: x = 121        Output: True   (reads 121 backward)
    Input: x = -121       Output: False  (reads 121- backward)
    Input: x = 10         Output: False  (reads 01 backward)
    Input: x = 0          Output: True   (single digit)

Follow-up:
    Could you solve it without converting the integer to a string?
"""


class Solution:
    def isPalindrome(self, x: int) -> bool:
        """
        Approach 1: String Conversion

        Convert the integer to a string and compare it with its reverse.

        Time Complexity:  O(n) where n is the number of digits
        Space Complexity: O(n) for the string representation

        Args:
            x: The integer to check.

        Returns:
            True if x is a palindrome, False otherwise.
        """
        s = str(x)
        return s == s[::-1]

    def isPalindromemath(self, x: int) -> bool:
        """
        Approach 2: Mathematical (Without Converting to String)

        Reverse the second half of the number and compare it with
        the first half. This avoids the overhead of string conversion
        and potential overflow issues in other languages.

        Key Observations:
            - Negative numbers are never palindromes (due to the '-' sign).
            - Numbers ending in 0 (except 0 itself) are never palindromes
              because no number starts with 0.
            - We only need to reverse HALF of the number and compare.

        Algorithm:
            1. Handle edge cases (negative, trailing zero).
            2. Repeatedly extract the last digit of x and build the
               reversed half.
            3. Stop when the reversed half >= remaining x.
            4. Compare x with reversed_half (even-digit case) or
               x with reversed_half // 10 (odd-digit case).

        Time Complexity:  O(log10(n)) -- we process half the digits
        Space Complexity: O(1) -- only a few integer variables

        Args:
            x: The integer to check.

        Returns:
            True if x is a palindrome, False otherwise.
        """
        # Edge case: negative numbers and numbers ending in 0 (except 0)
        if x < 0 or (x % 10 == 0 and x != 0):
            return False

        reversed_half = 0
        while x > reversed_half:
            # Extract the last digit and append to reversed_half
            reversed_half = reversed_half * 10 + x % 10
            # Remove the last digit from x
            x //= 10

        # Even number of digits: x == reversed_half
        # Odd number of digits:  x == reversed_half // 10
        #   (the middle digit doesn't matter for palindrome check)
        return x == reversed_half or x == reversed_half // 10


# 
# Test Cases
# 
if __name__ == "__main__":
    sol = Solution()

    #  Test Approach 1: String Conversion 

    # Basic palindromes
    assert sol.isPalindrome(121) is True, "121 is a palindrome"
    assert sol.isPalindrome(12321) is True, "12321 is a palindrome"
    assert sol.isPalindrome(1221) is True, "1221 is a palindrome"

    # Single digit numbers (always palindromes)
    assert sol.isPalindrome(0) is True, "0 is a palindrome"
    assert sol.isPalindrome(7) is True, "Single digit 7 is a palindrome"
    assert sol.isPalindrome(9) is True, "Single digit 9 is a palindrome"

    # Negative numbers (never palindromes)
    assert sol.isPalindrome(-121) is False, "Negative numbers are not palindromes"
    assert sol.isPalindrome(-1) is False, "-1 is not a palindrome"

    # Numbers ending in 0 (never palindromes, except 0 itself)
    assert sol.isPalindrome(10) is False, "10 is not a palindrome"
    assert sol.isPalindrome(100) is False, "100 is not a palindrome"
    assert sol.isPalindrome(1000) is False, "1000 is not a palindrome"

    # Non-palindrome numbers
    assert sol.isPalindrome(123) is False, "123 is not a palindrome"
    assert sol.isPalindrome(1234) is False, "1234 is not a palindrome"

    # Large palindrome
    assert sol.isPalindrome(1234321) is True, "1234321 is a palindrome"

    print(" Approach 1 (String Conversion): All test cases passed!")

    #  Test Approach 2: Mathematical 

    # Basic palindromes
    assert sol.isPalindromemath(121) is True, "121 is a palindrome"
    assert sol.isPalindromemath(12321) is True, "12321 is a palindrome"
    assert sol.isPalindromemath(1221) is True, "1221 is a palindrome"

    # Single digit numbers (always palindromes)
    assert sol.isPalindromemath(0) is True, "0 is a palindrome"
    assert sol.isPalindromemath(7) is True, "Single digit 7 is a palindrome"
    assert sol.isPalindromemath(9) is True, "Single digit 9 is a palindrome"

    # Negative numbers (never palindromes)
    assert sol.isPalindromemath(-121) is False, "Negative numbers are not palindromes"
    assert sol.isPalindromemath(-1) is False, "-1 is not a palindrome"

    # Numbers ending in 0 (never palindromes, except 0 itself)
    assert sol.isPalindromemath(10) is False, "10 is not a palindrome"
    assert sol.isPalindromemath(100) is False, "100 is not a palindrome"
    assert sol.isPalindromemath(1000) is False, "1000 is not a palindrome"

    # Non-palindrome numbers
    assert sol.isPalindromemath(123) is False, "123 is not a palindrome"
    assert sol.isPalindromemath(1234) is False, "1234 is not a palindrome"

    # Large palindrome
    assert sol.isPalindromemath(1234321) is True, "1234321 is a palindrome"

    print(" Approach 2 (Mathematical):      All test cases passed!")
    print()
    print(" All test cases passed!")
