"""
LeetCode 56 -- Merge Intervals (Advanced)
==========================================
Merge overlapping intervals with comprehensive edge case handling.
"""


def merge(intervals):
    """
    Sort by start time, then merge overlapping intervals.
    Time: O(n log n), Space: O(n)
    """
    if not intervals:
        return []

    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0][:]]  # Copy first interval

    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])

    return merged


if __name__ == "__main__":
    assert merge([[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]
    assert merge([[1, 4], [4, 5]]) == [[1, 5]]           # touching
    assert merge([[1, 4], [0, 4]]) == [[0, 4]]           # unsorted
    assert merge([[1, 4], [2, 3]]) == [[1, 4]]           # contained
    assert merge([[1, 10], [2, 3], [4, 5]]) == [[1, 10]] # multiple contained
    assert merge([[1, 4]]) == [[1, 4]]                    # single
    assert merge([]) == []                                 # empty
    assert merge([[1, 1]]) == [[1, 1]]                    # point interval

    print("All test cases passed")
