"""
HackerRank -- Nested Lists
==========================

Problem:
    Given the names and grades of N students, store them in a nested list and
    print the name(s) of any student(s) having the second lowest grade.

    If there are multiple students with the second lowest grade, order their
    names alphabetically and print each name on a new line.

Example:
    Students:
        Harry   37.21
        Berry   37.21
        Tina    37.2
        Akriti  41.0
        Harsh   39.0

    The lowest grade is 37.2 (Tina).
    The second lowest grade is 37.21 (Harry and Berry).
    Alphabetically ordered: Berry, Harry

    Output:
        Berry
        Harry

Approach:
    1. Store each student as [name, grade] in a nested list.
    2. Extract unique grades and sort them.
    3. Identify the second lowest grade.
    4. Filter students who have that grade.
    5. Sort those names alphabetically and print each.
"""


def find_second_lowest(students: list[list]) -> list[str]:
    """
    Given a nested list of [name, grade] pairs, return the names of students
    with the second lowest grade, sorted alphabetically.

    Parameters:
        students: list of [name: str, grade: float] pairs

    Returns:
        list of names (str) sorted alphabetically
    """
    # Step 1: Extract all unique grades
    grades = set()
    for student in students:
        grades.add(student[1])

    # Step 2: Sort grades in ascending order
    sorted_grades = sorted(grades)

    # Edge case: if there's only one unique grade, no second lowest exists
    if len(sorted_grades) < 2:
        return []

    # Step 3: Identify the second lowest grade
    second_lowest = sorted_grades[1]

    # Step 4: Collect names of students with the second lowest grade
    names = []
    for student in students:
        if student[1] == second_lowest:
            names.append(student[0])

    # Step 5: Sort names alphabetically
    names.sort()

    return names


def find_second_lowest_comprehension(students: list[list]) -> list[str]:
    """
    Same logic using more Pythonic constructs (set comprehension,
    list comprehension, sorted).
    """
    # Get sorted unique grades
    sorted_grades = sorted({grade for _, grade in students})

    if len(sorted_grades) < 2:
        return []

    second_lowest = sorted_grades[1]

    # Filter and sort in one step
    return sorted(name for name, grade in students if grade == second_lowest)


# =============================================================================
# Sample Data & Tests
# =============================================================================
if __name__ == "__main__":

    # ---- Sample data: at least 5 students, some with the same grade ----
    students = [
        ["Harry",   37.21],
        ["Berry",   37.21],
        ["Tina",    37.2],
        ["Akriti",  41.0],
        ["Harsh",   39.0],
        ["Dinesh",  37.21],
        ["Priya",   39.0],
    ]

    # ---- Test Case 1: Main example ----
    expected_1 = ["Berry", "Dinesh", "Harry"]  # second lowest = 37.21
    result_1 = find_second_lowest(students)
    assert result_1 == expected_1, (
        f"Test 1 FAILED: got {result_1}, expected {expected_1}"
    )

    # Cross-check with comprehension approach
    result_1b = find_second_lowest_comprehension(students)
    assert result_1b == expected_1, (
        f"Test 1b FAILED: got {result_1b}, expected {expected_1}"
    )

    # ---- Test Case 2: Two students, distinct grades ----
    students_2 = [
        ["Alice", 90.0],
        ["Bob",   85.0],
    ]
    expected_2 = ["Alice"]  # second lowest = 90.0
    result_2 = find_second_lowest(students_2)
    assert result_2 == expected_2, (
        f"Test 2 FAILED: got {result_2}, expected {expected_2}"
    )

    # ---- Test Case 3: Multiple students sharing both lowest and second lowest ----
    students_3 = [
        ["Zara",    50.0],
        ["Yusuf",   50.0],
        ["Xerxes",  60.0],
        ["Wendy",   60.0],
        ["Victor",  70.0],
    ]
    expected_3 = ["Wendy", "Xerxes"]  # second lowest = 60.0
    result_3 = find_second_lowest(students_3)
    assert result_3 == expected_3, (
        f"Test 3 FAILED: got {result_3}, expected {expected_3}"
    )

    # ---- Test Case 4: All same grade -- no second lowest ----
    students_4 = [
        ["A", 80.0],
        ["B", 80.0],
        ["C", 80.0],
    ]
    expected_4 = []  # Only one unique grade
    result_4 = find_second_lowest(students_4)
    assert result_4 == expected_4, (
        f"Test 4 FAILED: got {result_4}, expected {expected_4}"
    )

    # ---- Test Case 5: Single student ----
    students_5 = [["Solo", 99.9]]
    expected_5 = []
    result_5 = find_second_lowest(students_5)
    assert result_5 == expected_5, (
        f"Test 5 FAILED: got {result_5}, expected {expected_5}"
    )

    # ---- Print formatted output for the main example ----
    print("=" * 50)
    print("Students with the Second Lowest Grade:")
    print("=" * 50)
    for name in result_1:
        print(name)
    print()

    print("All test cases passed!")
