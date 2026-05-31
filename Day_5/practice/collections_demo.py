"""
Collections Module Demo
========================
Practical examples of Counter, defaultdict, deque, OrderedDict, namedtuple.
"""

from collections import Counter, defaultdict, deque, OrderedDict, namedtuple

print("=" * 50)
print("  COLLECTIONS MODULE DEMO")
print("=" * 50)

# ============================================================
# 1. COUNTER
# ============================================================

print("\n--- Counter ---")

# Frequency of words
text = "apple banana apple cherry banana apple date cherry"
word_count = Counter(text.split())
print(f"Word count: {word_count}")
print(f"Most common 2: {word_count.most_common(2)}")

# Character frequency
char_count = Counter("mississippi")
print(f"'mississippi': {char_count}")

# Counter arithmetic
c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=2)
print(f"c1 + c2 = {c1 + c2}")
print(f"c1 - c2 = {c1 - c2}")  # Only positive counts

# Real-world: Log level analysis
logs = ["INFO", "ERROR", "INFO", "WARN", "ERROR", "INFO", "DEBUG", "ERROR"]
log_stats = Counter(logs)
print(f"Log stats: {log_stats}")

# ============================================================
# 2. DEFAULTDICT
# ============================================================

print("\n--- defaultdict ---")

# Group items by category
items = [
    ("fruit", "apple"), ("veggie", "carrot"), ("fruit", "banana"),
    ("veggie", "peas"), ("fruit", "cherry"), ("grain", "rice"),
]
grouped = defaultdict(list)
for category, item in items:
    grouped[category].append(item)
print(f"Grouped: {dict(grouped)}")

# Count with defaultdict(int)
words = "the cat sat on the mat the cat".split()
word_freq = defaultdict(int)
for word in words:
    word_freq[word] += 1
print(f"Frequency: {dict(word_freq)}")

# Nested defaultdict
org = defaultdict(lambda: defaultdict(list))
org["Engineering"]["backend"].append("Alice")
org["Engineering"]["frontend"].append("Bob")
org["Sales"]["regional"].append("Charlie")
print(f"Org: {dict({k: dict(v) for k, v in org.items()})}")

# ============================================================
# 3. DEQUE (Double-Ended Queue)
# ============================================================

print("\n--- deque ---")

# Basic operations
dq = deque([1, 2, 3, 4, 5])
print(f"Initial: {dq}")

dq.appendleft(0)
print(f"appendleft(0): {dq}")

dq.append(6)
print(f"append(6): {dq}")

dq.popleft()
print(f"popleft(): {dq}")

dq.rotate(2)   # rotate right
print(f"rotate(2): {dq}")

dq.rotate(-2)  # rotate left
print(f"rotate(-2): {dq}")

# Fixed-size deque (sliding window)
print("\nFixed-size deque (maxlen=3):")
recent = deque(maxlen=3)
for item in ["a", "b", "c", "d", "e"]:
    recent.append(item)
    print(f"  Added '{item}': {list(recent)}")

# BFS level order example
print("\nBFS simulation:")
graph = {1: [2, 3], 2: [4], 3: [5], 4: [], 5: []}
queue = deque([1])
visited = set()
order = []
while queue:
    node = queue.popleft()
    if node not in visited:
        visited.add(node)
        order.append(node)
        queue.extend(graph.get(node, []))
print(f"  BFS order: {order}")

# ============================================================
# 4. ORDEREDDICT
# ============================================================

print("\n--- OrderedDict ---")

# Note: dict preserves insertion order since Python 3.7
# but OrderedDict has extra methods

od = OrderedDict()
od["first"] = 1
od["second"] = 2
od["third"] = 3
print(f"OrderedDict: {od}")

# move_to_end
od.move_to_end("first")
print(f"move_to_end('first'): {od}")

od.move_to_end("third", last=False)  # Move to beginning
print(f"move_to_end('third', last=False): {od}")

# popitem -- LIFO by default
item = od.popitem()
print(f"popitem(): {item}, remaining: {od}")

# ============================================================
# 5. NAMEDTUPLE
# ============================================================

print("\n--- namedtuple ---")

# Define a named tuple
Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
print(f"Point: {p}")
print(f"x={p.x}, y={p.y}")

# Employee record
Employee = namedtuple("Employee", "name department salary")
emp = Employee("Alice", "Engineering", 85000)
print(f"Employee: {emp}")
print(f"Name: {emp.name}, Dept: {emp.department}")

# Convert to dict
print(f"As dict: {emp._asdict()}")

# Create from dict
data = {"name": "Bob", "department": "Sales", "salary": 65000}
emp2 = Employee(**data)
print(f"From dict: {emp2}")

# Replace (creates new tuple)
emp3 = emp._replace(salary=90000)
print(f"After raise: {emp3}")
