"""
LeetCode 36 -- Valid Sudoku
==========================
Difficulty: Medium
Link: https://leetcode.com/problems/valid-sudoku/

Problem Description:
    Determine if a 9 x 9 Sudoku board is valid. Only the filled cells need
    to be validated according to the following rules:

    1. Each row must contain the digits 1-9 without repetition.
    2. Each column must contain the digits 1-9 without repetition.
    3. Each of the nine 3 x 3 sub-boxes of the grid must contain the
       digits 1-9 without repetition.

    Note:
    - A Sudoku board (partially filled) could be valid but is not
      necessarily solvable.
    - Only the filled cells need to be validated according to the
      mentioned rules.

Approach:
    Use three sets to track digits seen so far:
    - rows[i]  : set of digits seen in row i
    - cols[j]  : set of digits seen in column j
    - boxes[k] : set of digits seen in 3x3 box k

    The box index for cell (i, j) is calculated as:
        k = (i // 3) * 3 + (j // 3)

    For each filled cell, check if the digit already exists in any of
    the three sets. If yes, the board is invalid. Otherwise, add the
    digit to all three sets.

Time Complexity:  O(81) = O(1) -- fixed 9x9 board
Space Complexity: O(81) = O(1) -- at most 81 elements across all sets
"""

from typing import List


def is_valid_sudoku(board: List[List[str]]) -> bool:
    """
    Check if a 9x9 Sudoku board is valid.

    Args:
        board: 9x9 list of strings where '.' represents empty cells
               and '1'-'9' represent filled cells.

    Returns:
        True if the board is valid, False otherwise.
    """
    # Initialize sets for each row, column, and 3x3 box
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]

    for i in range(9):
        for j in range(9):
            digit = board[i][j]

            # Skip empty cells
            if digit == ".":
                continue

            # Calculate which 3x3 box this cell belongs to
            box_index = (i // 3) * 3 + (j // 3)

            # Check if digit already exists in row, column, or box
            if digit in rows[i]:
                return False
            if digit in cols[j]:
                return False
            if digit in boxes[box_index]:
                return False

            # Add digit to the corresponding row, column, and box sets
            rows[i].add(digit)
            cols[j].add(digit)
            boxes[box_index].add(digit)

    return True


# ============================================================
# Test Cases
# ============================================================

# Test 1: Valid Sudoku board
valid_board = [
    ["5", "3", ".", ".", "7", ".", ".", ".", "."],
    ["6", ".", ".", "1", "9", "5", ".", ".", "."],
    [".", "9", "8", ".", ".", ".", ".", "6", "."],
    ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
    ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
    ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
    [".", "6", ".", ".", ".", ".", "2", "8", "."],
    [".", ".", ".", "4", "1", "9", ".", ".", "5"],
    [".", ".", ".", ".", "8", ".", ".", "7", "9"],
]
assert is_valid_sudoku(valid_board) is True, "Test 1 Failed: Valid board"

# Test 2: Invalid Sudoku board (duplicate '8' in top-left 3x3 box)
invalid_board = [
    ["8", "3", ".", ".", "7", ".", ".", ".", "."],
    ["6", ".", ".", "1", "9", "5", ".", ".", "."],
    [".", "9", "8", ".", ".", ".", ".", "6", "."],
    ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
    ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
    ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
    [".", "6", ".", ".", ".", ".", "2", "8", "."],
    [".", ".", ".", "4", "1", "9", ".", ".", "5"],
    [".", ".", ".", ".", "8", ".", ".", "7", "9"],
]
assert is_valid_sudoku(invalid_board) is False, "Test 2 Failed: Invalid board"

# Test 3: Empty board (all dots -- valid)
empty_board = [["." for _ in range(9)] for _ in range(9)]
assert is_valid_sudoku(empty_board) is True, "Test 3 Failed: Empty board"

# Test 4: Invalid board -- duplicate in same row
row_dup_board = [["." for _ in range(9)] for _ in range(9)]
row_dup_board[0][0] = "1"
row_dup_board[0][8] = "1"  # Duplicate '1' in row 0
assert is_valid_sudoku(row_dup_board) is False, "Test 4 Failed: Row duplicate"

# Test 5: Invalid board -- duplicate in same column
col_dup_board = [["." for _ in range(9)] for _ in range(9)]
col_dup_board[0][0] = "5"
col_dup_board[8][0] = "5"  # Duplicate '5' in column 0
assert is_valid_sudoku(col_dup_board) is False, "Test 5 Failed: Column duplicate"

# Test 6: Invalid board -- duplicate in same 3x3 box
box_dup_board = [["." for _ in range(9)] for _ in range(9)]
box_dup_board[0][0] = "3"
box_dup_board[2][2] = "3"  # Duplicate '3' in top-left 3x3 box
assert is_valid_sudoku(box_dup_board) is False, "Test 6 Failed: Box duplicate"

# Test 7: Single filled cell (valid)
single_board = [["." for _ in range(9)] for _ in range(9)]
single_board[4][4] = "7"
assert is_valid_sudoku(single_board) is True, "Test 7 Failed: Single cell"

print("All test cases passed!")
