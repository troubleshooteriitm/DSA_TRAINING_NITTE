"""
LeetCode 56 -- Merge Intervals
================================
Given an array of intervals where intervals[i] = [start_i, end_i],
merge all overlapping intervals.

Example:
    Input:  [[1,3],[2,6],[8,10],[15,18]]
    Output: [[1,6],[8,10],[15,18]]

Approach: Sort by start time, then merge overlapping.
Time: O(n log n), Space: O(n)
"""


def merge_intervals(intervals):
    """Sort by start, merge overlapping intervals."""
    if not intervals:
        return []

    # Sort by start time
    intervals.sort(key=lambda x: x[0])

    merged = [intervals[0]]

    for current in intervals[1:]:
        last = merged[-1]
        if current[0] <= last[1]:
            # Overlapping -- extend the end
            last[1] = max(last[1], current[1])
        else:
            # No overlap -- add new interval
            merged.append(current)

    return merged


# ============================================================
# TESTS
# ============================================================

if __name__ == "__main__":
    assert merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]
    assert merge_intervals([[1, 4], [4, 5]]) == [[1, 5]]
    assert merge_intervals([[1, 4], [0, 4]]) == [[0, 4]]
    assert merge_intervals([[1, 4]]) == [[1, 4]]
    assert merge_intervals([]) == []
    assert merge_intervals([[1, 4], [2, 3]]) == [[1, 4]]  # fully contained
    assert merge_intervals([[1, 10], [2, 3], [4, 5], [6, 7]]) == [[1, 10]]

    print("All test cases passed")
