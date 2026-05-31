# Day 12 -- Advanced Python & Corporate Problem Solving

##  Topics Covered
- Multithreading & Multiprocessing
- GIL, REST APIs, Web Scraping concepts
- Performance Optimization
- Heapq, deque, Advanced Collections

---

## 1. Multithreading

```python
import threading
import time

def download_file(filename):
    print(f"Starting download: {filename}")
    time.sleep(2)  # Simulate I/O
    print(f"Completed: {filename}")

# Sequential: ~6 seconds
# Threaded: ~2 seconds (I/O bound)
threads = []
for f in ["file1.csv", "file2.csv", "file3.csv"]:
    t = threading.Thread(target=download_file, args=(f,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()  # Wait for all threads

print("All downloads complete!")
```

### Thread Lock (Synchronization)
```python
counter = 0
lock = threading.Lock()

def increment(n):
    global counter
    for _ in range(n):
        with lock:  # Thread-safe
            counter += 1

t1 = threading.Thread(target=increment, args=(100000,))
t2 = threading.Thread(target=increment, args=(100000,))
t1.start(); t2.start()
t1.join(); t2.join()
print(f"Counter: {counter}")  # Always 200000
```

---

## 2. Multiprocessing

```python
from multiprocessing import Process, Pool
import os

def cpu_task(n):
    """CPU-bound work -- benefits from multiprocessing."""
    return sum(i*i for i in range(n))

# Pool for parallel CPU work
with Pool(processes=4) as pool:
    results = pool.map(cpu_task, [10**6, 10**6, 10**6, 10**6])
```

### When to Use What?

| Scenario | Use | Why |
|----------|-----|-----|
| I/O bound (network, files) | `threading` | GIL is released during I/O |
| CPU bound (computation) | `multiprocessing` | Each process has its own GIL |
| Async I/O | `asyncio` | Single-thread, non-blocking |

---

## 3. GIL (Global Interpreter Lock)

- Python's GIL allows only **one thread to execute Python bytecode** at a time
- This means threading does NOT speed up CPU-bound tasks
- **I/O-bound tasks** release the GIL, so threading helps
- Use `multiprocessing` to bypass the GIL for CPU-bound tasks

---

## 4. REST API Basics

### HTTP Methods
| Method | Purpose | Example |
|--------|---------|---------|
| GET | Read | Fetch user list |
| POST | Create | Create new user |
| PUT | Update (full) | Update user profile |
| PATCH | Update (partial) | Change user email |
| DELETE | Remove | Delete user |

### Status Codes
| Code | Meaning |
|------|---------|
| 200 | OK |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 404 | Not Found |
| 500 | Internal Server Error |

```python
import requests  # pip install requests

# GET request
response = requests.get("https://api.example.com/users")
data = response.json()

# POST request
new_user = {"name": "Alice", "email": "alice@example.com"}
response = requests.post("https://api.example.com/users", json=new_user)
```

---

## 5. Heapq (Priority Queue)

```python
import heapq

# Min heap
nums = [5, 1, 8, 3, 2, 7]
heapq.heapify(nums)       # Convert to heap in-place
smallest = heapq.heappop(nums)  # Pop smallest (1)
heapq.heappush(nums, 0)          # Push new element

# Get N largest/smallest
data = [10, 1, 5, 8, 3, 12, 7, 2]
print(heapq.nlargest(3, data))    # [12, 10, 8]
print(heapq.nsmallest(3, data))   # [1, 2, 3]

# Priority queue pattern
tasks = [(3, "Low priority"), (1, "Critical"), (2, "Medium")]
heapq.heapify(tasks)
while tasks:
    priority, task = heapq.heappop(tasks)
    print(f"Processing: {task} (priority {priority})")
```

---

## 6. Deque for Streaming

```python
from collections import deque

# Sliding window (last N items)
recent_prices = deque(maxlen=5)
for price in [100, 102, 98, 105, 110, 108, 112]:
    recent_prices.append(price)
    avg = sum(recent_prices) / len(recent_prices)
    print(f"Price: {price}, Moving Avg: {avg:.1f}")
```

---

## 7. Performance Optimization

```python
import timeit

# 1. Use generators for large data
sum(x**2 for x in range(1000000))  # Generator -- memory efficient
sum([x**2 for x in range(1000000)]) # List -- stores all in memory

# 2. Use set for O(1) lookups
items_set = set(large_list)  # O(1) lookup
if item in items_set:        # vs O(n) for list
    pass

# 3. Use collections for specialized needs
from collections import Counter, defaultdict
# Counter.most_common() is faster than manual counting

# 4. Profile with cProfile
import cProfile
cProfile.run('my_function()')

# 5. Time with timeit
timeit.timeit('sum(range(1000))', number=10000)
```

---

##  Interview Tips
- Know the **GIL**: Threading helps I/O, multiprocessing helps CPU
- **Heapq**: Essential for top-K problems, merge K sorted lists
- **Deque**: O(1) operations on both ends vs O(n) for list.insert(0)
- REST APIs: Know HTTP methods, status codes, request/response cycle
- **Profiling first**: Don't optimize without measuring

##  Practice Problems
| Problem | Platform | Difficulty |
|---------|----------|------------|
| Longest Substring Without Repeating | LeetCode 3 | Medium |
| Top K Frequent Elements | LeetCode 347 | Medium |
| Merge Intervals | LeetCode 56 | Medium |
