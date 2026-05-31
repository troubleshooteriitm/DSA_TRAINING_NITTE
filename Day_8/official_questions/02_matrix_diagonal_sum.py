"""
LeetCode 1572 -- Matrix Diagonal Sum
====================================
Difficulty: Easy
Link: https://leetcode.com/problems/matrix-diagonal-sum/

Problem Description:
    Given a square matrix `mat`, return the sum of the matrix diagonals.
    Only include the sum of all the elements on the primary diagonal and
    all the elements on the secondary diagonal that are not part of the
    primary diagonal.

    - Primary diagonal: elements where row index == column index
      (top-left to bottom-right)
    - Secondary diagonal: elements where row + col == n - 1
      (top-right to bottom-left)

    If the matrix has odd dimensions, the center element is on BOTH
    diagonals, so it should only be counted once.

Approach:
    1. Iterate through each row index i.
    2. Add mat[i][i] (primary diagonal element).
    3. Add mat[i][n - 1 - i] (secondary diagonal element).
    4. If n is odd, subtract the center element (counted twice)
       at position mat[n//2][n//2].

Time Complexity:  O(n) -- single pass through diagonal indices
Space Complexity: O(1) -- no extra space used
"""

from typing import List


def diagonal_sum(mat: List[List[int]]) -> int:
    """
    Calculate the sum of primary and secondary diagonal elements.

    Args:
        mat: An n x n square matrix of integers.

    Returns:
        Sum of diagonal elements (center counted only once if n is odd).
    """
    n = len(mat)
    total = 0

    for i in range(n):
        # Add primary diagonal element (top-left to bottom-right)
        total += mat[i][i]

        # Add secondary diagonal element (top-right to bottom-left)
        total += mat[i][n - 1 - i]

    # If n is odd, the center element was counted twice -- subtract it once
    if n % 2 == 1:
        center = n // 2
        total -= mat[center][center]

    return total


# ============================================================
# Test Cases
# ============================================================

# Test 1: 3x3 matrix (odd dimension -- center element shared)
# Primary diagonal:   1 + 5 + 9 = 15
# Secondary diagonal: 3 + 5 + 7 = 15
# Center (5) counted twice, so subtract once: 15 + 15 - 5 = 25
mat1 = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]
assert diagonal_sum(mat1) == 25, f"Test 1 Failed: got {diagonal_sum(mat1)}"

# Test 2: 4x4 matrix (even dimension -- no shared center element)
# Primary diagonal:   1 + 6 + 11 + 16 = 34
# Secondary diagonal: 4 + 7 + 10 + 13 = 34
# Total: 34 + 34 = 68
mat2 = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16],
]
assert diagonal_sum(mat2) == 68, f"Test 2 Failed: got {diagonal_sum(mat2)}"

# Test 3: 1x1 matrix (single element is both diagonals)
mat3 = [[5]]
assert diagonal_sum(mat3) == 5, f"Test 3 Failed: got {diagonal_sum(mat3)}"

# Test 4: LeetCode Example 2
# Primary: 1 + 5 + 9 = 15
# Secondary: 3 + 5 + 7 = 15
# Subtract center: 15 + 15 - 5 = 25
mat4 = [
    [1, 1, 1, 1],
    [1, 1, 1, 1],
    [1, 1, 1, 1],
    [1, 1, 1, 1],
]
assert diagonal_sum(mat4) == 8, f"Test 4 Failed: got {diagonal_sum(mat4)}"

# Test 5: 2x2 matrix
# Primary: 1 + 4 = 5, Secondary: 2 + 3 = 5, Total = 10
mat5 = [
    [1, 2],
    [3, 4],
]
assert diagonal_sum(mat5) == 10, f"Test 5 Failed: got {diagonal_sum(mat5)}"

# Test 6: 5x5 matrix with zeros
mat6 = [
    [1, 0, 0, 0, 1],
    [0, 1, 0, 1, 0],
    [0, 0, 1, 0, 0],
    [0, 1, 0, 1, 0],
    [1, 0, 0, 0, 1],
]
# Primary: 1+1+1+1+1 = 5, Secondary: 1+1+1+1+1 = 5, Center=1
# Total = 5 + 5 - 1 = 9
assert diagonal_sum(mat6) == 9, f"Test 6 Failed: got {diagonal_sum(mat6)}"

# Test 7: All zeros
mat7 = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]
assert diagonal_sum(mat7) == 0, f"Test 7 Failed: got {diagonal_sum(mat7)}"

# Test 8: Large values
mat8 = [
    [100, 0, 100],
    [0, 50, 0],
    [100, 0, 100],
]
# Primary: 100+50+100=250, Secondary: 100+50+100=250, Center=50
# Total = 250 + 250 - 50 = 450
assert diagonal_sum(mat8) == 450, f"Test 8 Failed: got {diagonal_sum(mat8)}"

print("All test cases passed!")
