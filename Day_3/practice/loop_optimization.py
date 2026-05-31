"""
Loop Optimization Techniques in Python -- Day 3 Practice
=========================================================

This module demonstrates six loop optimization techniques, each showing
the 'bad' (naive) way and the 'good' (optimized) way, with timing
comparisons where relevant.

Fully runnable -- just execute the file.
"""

import time
import sys


# =============================================================================
# Helper: Timer context manager for clean benchmarking
# =============================================================================
class Timer:
    """Simple context manager to measure elapsed time."""

    def __init__(self, label: str):
        self.label = label
        self.elapsed = 0.0

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, *args):
        self.elapsed = time.perf_counter() - self.start

    def __str__(self):
        return f"{self.label}: {self.elapsed:.6f} seconds"


# =============================================================================
# 1. Loop vs List Comprehension -- Timing Comparison
# =============================================================================
def demo_loop_vs_comprehension():
    """
    ============================================================
    1. LOOP vs LIST COMPREHENSION -- Timing Comparison
    ============================================================
    List comprehensions are generally faster than equivalent
    for-loops because they are optimized at the C level in
    CPython and avoid the overhead of repeated .append() calls.
    """
    print(demo_loop_vs_comprehension.__doc__)

    N = 1_000_000

    #  BAD: Traditional for-loop with append
    with Timer("  Traditional loop") as t_loop:
        squares_loop = []
        for x in range(N):
            squares_loop.append(x ** 2)
    print(t_loop)

    #  GOOD: List comprehension
    with Timer("  List comprehension") as t_comp:
        squares_comp = [x ** 2 for x in range(N)]
    print(t_comp)

    # Verify same result
    assert squares_loop == squares_comp, "Results should be identical!"

    if t_loop.elapsed > 0:
        speedup = t_loop.elapsed / t_comp.elapsed
        print(f"  Speedup: {speedup:.2f}x faster with list comprehension\n")

    #  BAD: Filtered loop
    with Timer("  Filtered loop") as t_filt_loop:
        evens_loop = []
        for x in range(N):
            if x % 2 == 0:
                evens_loop.append(x)
    print(t_filt_loop)

    #  GOOD: Filtered list comprehension
    with Timer("  Filtered comprehension") as t_filt_comp:
        evens_comp = [x for x in range(N) if x % 2 == 0]
    print(t_filt_comp)

    assert evens_loop == evens_comp
    print()


# =============================================================================
# 2. enumerate() vs Manual Index Counter
# =============================================================================
def demo_enumerate():
    """
    ============================================================
    2. enumerate() vs MANUAL INDEX COUNTER
    ============================================================
    enumerate() is cleaner, less error-prone, and slightly
    faster than maintaining a manual counter variable.
    """
    print(demo_enumerate.__doc__)

    fruits = ["apple", "banana", "cherry", "date", "elderberry",
              "fig", "grape", "honeydew", "kiwi", "lemon"]

    #  BAD: Manual index tracking
    print("   Manual index:")
    index = 0
    for fruit in fruits:
        print(f"     {index}: {fruit}")
        index += 1

    print()

    #  GOOD: Using enumerate
    print("   Using enumerate():")
    for index, fruit in enumerate(fruits):
        print(f"     {index}: {fruit}")

    print()

    #  GOOD: enumerate with custom start
    print("   enumerate(start=1) -- 1-based numbering:")
    for rank, fruit in enumerate(fruits[:5], start=1):
        print(f"     {rank}. {fruit}")

    print()


# =============================================================================
# 3. zip() for Parallel Iteration
# =============================================================================
def demo_zip():
    """
    ============================================================
    3. zip() for PARALLEL ITERATION
    ============================================================
    zip() is the idiomatic way to iterate over multiple sequences
    simultaneously, replacing error-prone manual indexing.
    """
    print(demo_zip.__doc__)

    names = ["Alice", "Bob", "Charlie", "Diana", "Eve"]
    scores = [95, 82, 78, 91, 88]
    grades = ["A", "B+", "C+", "A", "B+"]

    #  BAD: Manual indexing
    print("   Manual indexing:")
    for i in range(len(names)):
        print(f"     {names[i]}: Score={scores[i]}, Grade={grades[i]}")

    print()

    #  GOOD: Using zip
    print("   Using zip():")
    for name, score, grade in zip(names, scores, grades):
        print(f"     {name}: Score={score}, Grade={grade}")

    print()

    #  BONUS: Creating a dict from two lists using zip
    print("   Creating dict with zip():")
    score_dict = dict(zip(names, scores))
    for name, score in score_dict.items():
        print(f"     {name} -> {score}")

    print()


# =============================================================================
# 4. break / continue -- Practical Examples
# =============================================================================
def demo_break_continue():
    """
    ============================================================
    4. break / continue -- Practical Examples
    ============================================================
    break: Exit the loop early when the goal is achieved.
    continue: Skip unwanted iterations without nesting more ifs.
    """
    print(demo_break_continue.__doc__)

    # --- break: Searching for a value ---
    print("  --- break: Finding first prime > 100 ---")
    for num in range(101, 200):
        is_prime = True
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                is_prime = False
                break  # No need to check further divisors
        if is_prime:
            print(f"     First prime > 100: {num}")
            break  # Found it; stop the outer loop too

    print()

    # --- continue: Filtering while iterating ---
    print("  --- continue: Processing only valid data ---")
    raw_data = [42, -3, "N/A", 17, None, 0, 88, "", 55, -1]
    clean_data = []
    for item in raw_data:
        # Skip non-positive and non-numeric items
        if not isinstance(item, (int, float)):
            continue
        if item <= 0:
            continue
        clean_data.append(item)

    print(f"     Raw data:   {raw_data}")
    print(f"     Clean data: {clean_data}")

    print()

    # --- break with else: Search with feedback ---
    print("  --- for/else: Search with 'not found' fallback ---")
    users = ["alice", "bob", "charlie", "diana"]
    search_for = "eve"
    for user in users:
        if user == search_for:
            print(f"     Found user: {user}")
            break
    else:
        print(f"     User '{search_for}' not found in the list")

    print()


# =============================================================================
# 5. Avoiding Repeated Computation Inside Loops
# =============================================================================
def demo_avoid_repeated_computation():
    """
    ============================================================
    5. AVOIDING REPEATED COMPUTATION Inside Loops
    ============================================================
    Move invariant calculations outside the loop. Cache values
    like len(), computed constants, and method lookups.
    """
    print(demo_avoid_repeated_computation.__doc__)

    data = list(range(1, 1_000_001))

    #  BAD: Calling len() inside the loop every iteration
    with Timer("  len() inside loop") as t_bad:
        total_bad = 0
        for i in range(len(data)):
            total_bad += data[i] / len(data)  # len(data) recalculated!
    print(t_bad)

    #  GOOD: Pre-compute len()
    with Timer("  len() pre-computed") as t_good:
        total_good = 0
        n = len(data)
        for i in range(n):
            total_good += data[i] / n
    print(t_good)

    if t_bad.elapsed > 0:
        speedup = t_bad.elapsed / t_good.elapsed
        print(f"  Speedup: {speedup:.2f}x faster\n")

    # Another example: pre-compute a constant
    print("  --- Pre-computing a constant ---")

    import math

    #  BAD: Recomputing sqrt inside loop
    with Timer("  sqrt in loop") as t_sqrt_bad:
        results_bad = []
        for x in range(100_000):
            results_bad.append(x * math.sqrt(2))
    print(t_sqrt_bad)

    #  GOOD: Pre-compute sqrt(2)
    with Timer("  sqrt pre-computed") as t_sqrt_good:
        results_good = []
        sqrt_2 = math.sqrt(2)
        for x in range(100_000):
            results_good.append(x * sqrt_2)
    print(t_sqrt_good)

    print()


# =============================================================================
# 6. Generator Expressions vs List Comprehension (Memory Efficiency)
# =============================================================================
def demo_generator_vs_list():
    """
    ============================================================
    6. GENERATOR EXPRESSIONS vs LIST COMPREHENSION
    ============================================================
    Generators produce items lazily (one at a time) instead of
    building the entire list in memory. Use generators when you
    only need to iterate once (e.g., sum, any, all, max, min).
    """
    print(demo_generator_vs_list.__doc__)

    N = 1_000_000

    #  BAD: List comprehension -- stores all N items in memory
    with Timer("  List comprehension sum") as t_list:
        total_list = sum([x ** 2 for x in range(N)])
    print(t_list)

    #  GOOD: Generator expression -- constant memory
    with Timer("  Generator expression sum") as t_gen:
        total_gen = sum(x ** 2 for x in range(N))
    print(t_gen)

    assert total_list == total_gen, "Results should be identical!"

    # Memory comparison (approximate)
    sample_list = [x ** 2 for x in range(N)]
    sample_gen = (x ** 2 for x in range(N))

    list_size = sys.getsizeof(sample_list)
    gen_size = sys.getsizeof(sample_gen)

    print(f"\n  Memory -- list: {list_size:,} bytes")
    print(f"  Memory -- generator: {gen_size:,} bytes")
    print(f"  Ratio: list is ~{list_size // gen_size}x larger in overhead\n")

    # Practical: any() with generator -- short-circuits on first True
    print("  --- any() with generator (short-circuit) ---")
    large_list = list(range(1_000_000))

    with Timer("  any() with generator") as t_any:
        found = any(x > 999_990 for x in large_list)
    print(f"  {t_any}  (found={found})")

    print()


# =============================================================================
# Main -- Run all demonstrations
# =============================================================================
if __name__ == "__main__":
    banner = """
    
             LOOP OPTIMIZATION TECHNIQUES IN PYTHON             
                      Day 3 -- Practice Module                   
    
    """
    print(banner)

    demo_loop_vs_comprehension()
    demo_enumerate()
    demo_zip()
    demo_break_continue()
    demo_avoid_repeated_computation()
    demo_generator_vs_list()

    print("=" * 60)
    print("  All loop optimization demonstrations completed!")
    print("=" * 60)
