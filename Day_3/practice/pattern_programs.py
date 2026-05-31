"""
Pattern Programs -- Day 3 Practice
===================================

Six classic pattern programs using nested loops.
Each function takes `n` (number of rows) as a parameter,
prints the pattern, and includes a docstring showing expected
output for n=5.
"""


# =============================================================================
# 1. Right Triangle (Stars)
# =============================================================================
def right_triangle(n: int):
    """
    Print a right-aligned triangle of stars.

    Expected output for n=5:
        *
        **
        ***
        ****
        *****
    """
    for i in range(1, n + 1):
        print('*' * i)


# =============================================================================
# 2. Inverted Right Triangle (Stars)
# =============================================================================
def inverted_right_triangle(n: int):
    """
    Print an inverted right triangle of stars.

    Expected output for n=5:
        *****
        ****
        ***
        **
        *
    """
    for i in range(n, 0, -1):
        print('*' * i)


# =============================================================================
# 3. Pyramid (Centered Stars)
# =============================================================================
def pyramid(n: int):
    """
    Print a centered pyramid of stars.

    Expected output for n=5:
            *
           ***
          *****
         *******
        *********
    """
    for i in range(1, n + 1):
        spaces = ' ' * (n - i)
        stars = '*' * (2 * i - 1)
        print(spaces + stars)


# =============================================================================
# 4. Diamond (Combination of Pyramid and Inverted Pyramid)
# =============================================================================
def diamond(n: int):
    """
    Print a diamond pattern. The widest row has (2*n - 1) stars.

    Expected output for n=5:
            *
           ***
          *****
         *******
        *********
         *******
          *****
           ***
            *
    """
    # Upper half (pyramid)
    for i in range(1, n + 1):
        spaces = ' ' * (n - i)
        stars = '*' * (2 * i - 1)
        print(spaces + stars)

    # Lower half (inverted pyramid, starting from n-1)
    for i in range(n - 1, 0, -1):
        spaces = ' ' * (n - i)
        stars = '*' * (2 * i - 1)
        print(spaces + stars)


# =============================================================================
# 5. Number Triangle
# =============================================================================
def number_triangle(n: int):
    """
    Print a triangle where each row i contains numbers 1 through i.

    Expected output for n=5:
        1
        12
        123
        1234
        12345
    """
    for i in range(1, n + 1):
        for j in range(1, i + 1):
            print(j, end='')
        print()


# =============================================================================
# 6. Floyd's Triangle
# =============================================================================
def floyds_triangle(n: int):
    """
    Print Floyd's Triangle -- consecutive natural numbers filling rows.
    Row 1 has 1 number, row 2 has 2 numbers, row 3 has 3, etc.

    Expected output for n=5:
        1
        2 3
        4 5 6
        7 8 9 10
        11 12 13 14 15
    """
    num = 1
    for i in range(1, n + 1):
        for j in range(1, i + 1):
            print(num, end=' ')
            num += 1
        print()


# =============================================================================
# Main -- Run all patterns with n=5
# =============================================================================
if __name__ == "__main__":
    n = 5
    separator = "\n" + "=" * 40 + "\n"

    print("=" * 40)
    print(f"  PATTERN PROGRAMS (n = {n})")
    print("=" * 40)

    print(separator + "1. Right Triangle" + separator)
    right_triangle(n)

    print(separator + "2. Inverted Right Triangle" + separator)
    inverted_right_triangle(n)

    print(separator + "3. Pyramid" + separator)
    pyramid(n)

    print(separator + "4. Diamond" + separator)
    diamond(n)

    print(separator + "5. Number Triangle" + separator)
    number_triangle(n)

    print(separator + "6. Floyd's Triangle" + separator)
    floyds_triangle(n)

    print(separator + "All pattern programs executed successfully!")
