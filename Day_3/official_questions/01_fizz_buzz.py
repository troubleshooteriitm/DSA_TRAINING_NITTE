"""
LeetCode 412 -- Fizz Buzz (Loop-Focused Approach)
=================================================

Problem:
    Given an integer n, return a string array answer (1-indexed) where:
        - answer[i] == "FizzBuzz" if i is divisible by 3 and 5
        - answer[i] == "Fizz"     if i is divisible by 3
        - answer[i] == "Buzz"     if i is divisible by 5
        - answer[i] == str(i)     if none of the above conditions are true

Example 1:
    Input:  n = 3
    Output: ["1", "2", "Fizz"]

Example 2:
    Input:  n = 5
    Output: ["1", "2", "Fizz", "4", "Buzz"]

Example 3:
    Input:  n = 15
    Output: ["1","2","Fizz","4","Buzz","Fizz","7","8","Fizz","Buzz",
             "11","Fizz","13","14","FizzBuzz"]

Day 3 Focus:
    This version emphasizes LOOP constructs (for loops, conditionals inside
    loops, list building) and contrasts with a Pythonic list comprehension
    approach.

Constraints:
    1 <= n <= 10^4
"""


class Solution:
    # -------------------------------------------------------------------------
    # Approach 1: Basic Loop with if-elif-else
    # -------------------------------------------------------------------------
    def fizzBuzz(self, n: int) -> list[str]:
        """
        Build the answer list using a straightforward for-loop and
        conditional chain.

        Time Complexity : O(n)
        Space Complexity: O(n) for the result list
        """
        result = []
        for i in range(1, n + 1):
            if i % 15 == 0:          # divisible by both 3 and 5
                result.append("FizzBuzz")
            elif i % 3 == 0:         # divisible by 3 only
                result.append("Fizz")
            elif i % 5 == 0:         # divisible by 5 only
                result.append("Buzz")
            else:
                result.append(str(i))
        return result

    # -------------------------------------------------------------------------
    # Approach 2: Pythonic List Comprehension (one-liner)
    # -------------------------------------------------------------------------
    def fizzBuzz_comprehension(self, n: int) -> list[str]:
        """
        Same logic expressed as a single list comprehension using
        Python's conditional (ternary) expression.

        Time Complexity : O(n)
        Space Complexity: O(n)
        """
        return [
            "FizzBuzz" if i % 15 == 0
            else "Fizz" if i % 3 == 0
            else "Buzz" if i % 5 == 0
            else str(i)
            for i in range(1, n + 1)
        ]

    # -------------------------------------------------------------------------
    # Approach 3: String Concatenation Loop (extensible for more divisors)
    # -------------------------------------------------------------------------
    def fizzBuzz_concat(self, n: int) -> list[str]:
        """
        Build each label by concatenating parts. This approach scales well
        if more divisor-word mappings are added (e.g., 7 -> 'Jazz').

        Time Complexity : O(n * m) where m is the number of mappings
        Space Complexity: O(n)
        """
        mappings = [(3, "Fizz"), (5, "Buzz")]  # easy to extend
        result = []
        for i in range(1, n + 1):
            label = ""
            for divisor, word in mappings:
                if i % divisor == 0:
                    label += word
            if not label:
                label = str(i)
            result.append(label)
        return result


# =============================================================================
# Test Cases
# =============================================================================
if __name__ == "__main__":
    sol = Solution()

    expected_3 = ["1", "2", "Fizz"]
    expected_5 = ["1", "2", "Fizz", "4", "Buzz"]
    expected_15 = [
        "1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz",
        "11", "Fizz", "13", "14", "FizzBuzz"
    ]

    # Test Approach 1 -- Basic Loop
    assert sol.fizzBuzz(3) == expected_3, f"Failed: fizzBuzz(3)"
    assert sol.fizzBuzz(5) == expected_5, f"Failed: fizzBuzz(5)"
    assert sol.fizzBuzz(15) == expected_15, f"Failed: fizzBuzz(15)"
    assert sol.fizzBuzz(1) == ["1"], f"Failed: fizzBuzz(1)"

    # Test Approach 2 -- List Comprehension
    assert sol.fizzBuzz_comprehension(3) == expected_3
    assert sol.fizzBuzz_comprehension(5) == expected_5
    assert sol.fizzBuzz_comprehension(15) == expected_15
    assert sol.fizzBuzz_comprehension(1) == ["1"]

    # Test Approach 3 -- String Concatenation
    assert sol.fizzBuzz_concat(3) == expected_3
    assert sol.fizzBuzz_concat(5) == expected_5
    assert sol.fizzBuzz_concat(15) == expected_15
    assert sol.fizzBuzz_concat(1) == ["1"]

    # Cross-check: all three approaches produce the same output
    for n in [1, 3, 5, 15, 30, 100]:
        r1 = sol.fizzBuzz(n)
        r2 = sol.fizzBuzz_comprehension(n)
        r3 = sol.fizzBuzz_concat(n)
        assert r1 == r2 == r3, f"Mismatch at n={n}"

    print("All test cases passed!")
