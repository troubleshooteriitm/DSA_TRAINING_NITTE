"""
Generators Demo
================
Practical generator examples: fibonacci, file reader, infinite counter,
chunked processing, and pipeline composition.
"""


# ============================================================
# 1. FIBONACCI GENERATOR
# ============================================================

def fibonacci(limit=None):
    """
    Generate Fibonacci numbers.
    If limit is None, generates infinitely.
    If limit is set, generates up to that many numbers.
    """
    a, b = 0, 1
    count = 0
    while limit is None or count < limit:
        yield a
        a, b = b, a + b
        count += 1


# ============================================================
# 2. FILE LINE READER (simulated)
# ============================================================

def line_reader(text):
    """
    Simulate reading a large file line by line.
    In production, you'd use: open(filepath) and yield each line.
    Memory-efficient: only one line in memory at a time.
    """
    for line in text.strip().split("\n"):
        yield line.strip()


# ============================================================
# 3. INFINITE COUNTER WITH STEP
# ============================================================

def counter(start=0, step=1):
    """Infinite counter -- use with next() or islice."""
    current = start
    while True:
        yield current
        current += step


# ============================================================
# 4. CHUNKED DATA PROCESSING
# ============================================================

def chunked(iterable, size):
    """
    Yield successive chunks of `size` from an iterable.
    Useful for batch processing large datasets.
    """
    chunk = []
    for item in iterable:
        chunk.append(item)
        if len(chunk) == size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk


# ============================================================
# 5. GENERATOR PIPELINE (Composing Generators)
# ============================================================

def read_sensor_data():
    """Simulate reading raw sensor data."""
    import random
    random.seed(42)
    for i in range(20):
        yield {"sensor_id": f"S{(i % 3) + 1}", "value": round(random.uniform(20, 45), 1)}


def filter_anomalies(data_stream, threshold=40.0):
    """Filter out readings above a threshold."""
    for reading in data_stream:
        if reading["value"] <= threshold:
            yield reading


def enrich_data(data_stream):
    """Add status field based on value."""
    for reading in data_stream:
        value = reading["value"]
        if value < 25:
            reading["status"] = "LOW"
        elif value < 35:
            reading["status"] = "NORMAL"
        else:
            reading["status"] = "WARNING"
        yield reading


# ============================================================
# 6. GENERATOR EXPRESSION vs LIST COMPREHENSION
# ============================================================

def memory_comparison():
    """Show the memory advantage of generators."""
    import sys

    # List comprehension -- all values in memory
    list_comp = [x ** 2 for x in range(10000)]
    list_size = sys.getsizeof(list_comp)

    # Generator expression -- lazy evaluation
    gen_exp = (x ** 2 for x in range(10000))
    gen_size = sys.getsizeof(gen_exp)

    return list_size, gen_size


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":
    print("=" * 50)
    print("  GENERATORS DEMO")
    print("=" * 50)

    # Fibonacci
    print("\n--- Fibonacci (first 15) ---")
    print(list(fibonacci(15)))

    # Line reader
    print("\n--- Line Reader ---")
    sample_log = """2025-01-01 INFO Server started
2025-01-01 ERROR Connection timeout
2025-01-01 WARN Disk usage 85%
2025-01-01 INFO Request processed"""
    for line in line_reader(sample_log):
        print(f"  > {line}")

    # Counter
    print("\n--- Counter (start=10, step=5, first 8) ---")
    c = counter(10, 5)
    print([next(c) for _ in range(8)])

    # Chunked
    print("\n--- Chunked Processing (batch size 4) ---")
    data = list(range(1, 15))
    for i, batch in enumerate(chunked(data, 4), 1):
        print(f"  Batch {i}: {batch}")

    # Generator pipeline
    print("\n--- Generator Pipeline (Sensor Data) ---")
    pipeline = enrich_data(filter_anomalies(read_sensor_data(), threshold=40.0))
    for reading in pipeline:
        print(f"  {reading['sensor_id']}: {reading['value']}°C [{reading['status']}]")

    # Memory comparison
    print("\n--- Memory Comparison ---")
    list_size, gen_size = memory_comparison()
    print(f"  List comprehension (10k items): {list_size:,} bytes")
    print(f"  Generator expression (10k items): {gen_size:,} bytes")
    print(f"  Generator uses {list_size // gen_size}x less memory!")
