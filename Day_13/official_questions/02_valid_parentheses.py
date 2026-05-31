"""
LeetCode 20 -- Valid Parentheses
================================
Difficulty: Easy
URL: https://leetcode.com/problems/valid-parentheses/

Problem Description:
    Given a string s containing just the characters '(', ')', '{', '}',
    '[' and ']', determine if the input string is valid.

    An input string is valid if:
    1. Open brackets must be closed by the same type of brackets.
    2. Open brackets must be closed in the correct order.
    3. Every close bracket has a corresponding open bracket of the same type.

Approach:
    Use a stack (Python list) to track opening brackets.

    1. Iterate through each character in the string.
    2. If it's an opening bracket, push it onto the stack.
    3. If it's a closing bracket:
       - Check if the stack is empty (no matching opener)  invalid
       - Check if the top of the stack matches  pop if yes, invalid if no
    4. After processing all characters, the stack must be empty for valid input.

    We use a dictionary to map closing brackets to their corresponding
    opening brackets for O(1) lookup.

Time Complexity: O(n) -- we traverse the string once
Space Complexity: O(n) -- worst case, all opening brackets pushed to stack
"""


def is_valid(s: str) -> bool:
    """
    Check if the given string of brackets is valid.

    Uses a stack-based approach where opening brackets are pushed
    onto the stack and closing brackets are matched against the
    top of the stack.

    Args:
        s: A string containing only bracket characters: ()[]{}

    Returns:
        True if the string has valid bracket matching, False otherwise.
    """
    # Map each closing bracket to its corresponding opening bracket
    bracket_map = {
        ')': '(',
        ']': '[',
        '}': '{'
    }

    # Stack to keep track of opening brackets
    stack = []

    for char in s:
        if char in bracket_map:
            # It's a closing bracket
            # Pop the top element if stack is non-empty, else use a dummy value
            top_element = stack.pop() if stack else '#'

            # Check if the popped element matches the expected opening bracket
            if top_element != bracket_map[char]:
                return False
        else:
            # It's an opening bracket -- push onto stack
            stack.append(char)

    # Valid only if all opening brackets have been matched (stack is empty)
    return len(stack) == 0


def is_valid_verbose(s: str) -> bool:
    """
    Alternative implementation with explicit handling for clarity.

    This version explicitly checks for opening vs closing brackets
    and provides a more verbose but readable implementation.

    Args:
        s: A string containing only bracket characters.

    Returns:
        True if brackets are properly matched and nested.
    """
    opening = {'(', '[', '{'}
    closing = {')', ']', '}'}
    pairs = {')': '(', ']': '[', '}': '{'}

    stack = []

    for i, char in enumerate(s):
        if char in opening:
            stack.append(char)
        elif char in closing:
            if not stack:
                # Closing bracket with no matching opener
                return False
            if stack[-1] != pairs[char]:
                # Mismatched bracket types
                return False
            stack.pop()

    return len(stack) == 0


# ============================================================
# Test Cases
# ============================================================

if __name__ == '__main__':

    # Test 1: Simple valid parentheses
    assert is_valid("()") is True

    # Test 2: Multiple valid bracket types
    assert is_valid("()[]{}") is True

    # Test 3: Mismatched brackets
    assert is_valid("(]") is False

    # Test 4: Nested valid brackets
    assert is_valid("([])") is True

    # Test 5: Complex nesting
    assert is_valid("{[()]}") is True

    # Test 6: Empty string (valid -- no unmatched brackets)
    assert is_valid("") is True

    # Test 7: Single opening bracket (invalid)
    assert is_valid("(") is False

    # Test 8: Single closing bracket (invalid)
    assert is_valid(")") is False

    # Test 9: Wrong order of closing
    assert is_valid("([)]") is False

    # Test 10: Long valid string
    assert is_valid("(((())))") is True

    # Test 11: Interleaved valid brackets
    assert is_valid("(){}[]") is True

    # Test 12: Unbalanced -- extra opening
    assert is_valid("((())") is False

    # Test 13: Unbalanced -- extra closing
    assert is_valid("(()))") is False

    # --- Also verify the verbose implementation ---
    assert is_valid_verbose("()[]{}") is True
    assert is_valid_verbose("(]") is False
    assert is_valid_verbose("{[()]}") is True
    assert is_valid_verbose("([)]") is False
    assert is_valid_verbose("") is True

    print("All test cases passed!")
