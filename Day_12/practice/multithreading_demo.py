"""
Multithreading Demo
====================
Examples: creating threads, locks, daemon threads, thread pool.
"""

import threading
import time
from concurrent.futures import ThreadPoolExecutor


# ============================================================
# 1. BASIC THREADING
# ============================================================

def task(name, duration):
    print(f"  [{threading.current_thread().name}] {name} started")
    time.sleep(duration)
    print(f"  [{threading.current_thread().name}] {name} completed ({duration}s)")


print("=" * 50)
print("  MULTITHREADING DEMO")
print("=" * 50)

print("\n--- Basic Threading ---")
threads = []
for i in range(3):
    t = threading.Thread(target=task, args=(f"Task-{i+1}", 0.5), name=f"Worker-{i+1}")
    threads.append(t)
    t.start()

for t in threads:
    t.join()
print("  All tasks done!")


# ============================================================
# 2. THREAD LOCK (Race Condition Prevention)
# ============================================================

print("\n--- Thread Lock ---")

counter = 0
lock = threading.Lock()


def safe_increment(n):
    global counter
    for _ in range(n):
        with lock:
            counter += 1


counter = 0
t1 = threading.Thread(target=safe_increment, args=(100000,))
t2 = threading.Thread(target=safe_increment, args=(100000,))
t1.start()
t2.start()
t1.join()
t2.join()
print(f"  Counter (with lock): {counter}")  # Always 200000


# ============================================================
# 3. DAEMON THREADS
# ============================================================

print("\n--- Daemon Thread ---")


def background_monitor():
    """Daemon thread that runs in background."""
    for i in range(3):
        print(f"  [Daemon] Monitoring... tick {i+1}")
        time.sleep(0.2)


daemon = threading.Thread(target=background_monitor, daemon=True)
daemon.start()
time.sleep(0.7)  # Let it run a bit
print("  Main thread continues (daemon will stop when main exits)")


# ============================================================
# 4. THREAD POOL EXECUTOR
# ============================================================

print("\n--- ThreadPoolExecutor ---")


def download_page(url):
    """Simulate downloading a web page."""
    time.sleep(0.3)
    return f"Downloaded {url} ({len(url)} chars)"


urls = [
    "https://example.com/page1",
    "https://example.com/page2",
    "https://example.com/page3",
    "https://example.com/page4",
    "https://example.com/page5",
]

start = time.perf_counter()
with ThreadPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(download_page, urls))

elapsed = time.perf_counter() - start
for r in results:
    print(f"  {r}")
print(f"  Completed in {elapsed:.2f}s (vs ~{len(urls)*0.3:.1f}s sequential)")


# ============================================================
# 5. PRODUCER-CONSUMER PATTERN
# ============================================================

print("\n--- Producer-Consumer ---")

from collections import deque

buffer = deque(maxlen=5)
buffer_lock = threading.Lock()
items_produced = 0
items_consumed = 0


def producer(n):
    global items_produced
    for i in range(n):
        item = f"item-{i+1}"
        with buffer_lock:
            buffer.append(item)
            items_produced += 1
        time.sleep(0.05)


def consumer(n):
    global items_consumed
    for _ in range(n):
        time.sleep(0.08)
        with buffer_lock:
            if buffer:
                item = buffer.popleft()
                items_consumed += 1


p = threading.Thread(target=producer, args=(10,))
c = threading.Thread(target=consumer, args=(10,))
p.start()
c.start()
p.join()
c.join()

print(f"  Produced: {items_produced}, Consumed: {items_consumed}")
print(f"  Buffer remaining: {list(buffer)}")
