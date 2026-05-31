# Day 5 -- Python Collections & Comprehensions

##  Topics Covered
- Lists, Tuples, Dictionaries, Sets, Frozen Sets
- List/Dict/Set Comprehensions
- Nested Collections, Slicing, Packing & Unpacking
- `enumerate()`, `zip()`
- `Counter`, `defaultdict`, `deque`, `OrderedDict`
- Iterators & Iterables

---

## 1. Lists

```python
# Creation
fruits = ["apple", "banana", "cherry"]
numbers = list(range(1, 6))  # [1, 2, 3, 4, 5]

# Common Methods
fruits.append("date")          # Add to end
fruits.insert(1, "blueberry")  # Insert at index
fruits.extend(["elderberry"])  # Add multiple
fruits.remove("banana")        # Remove by value
popped = fruits.pop()          # Remove & return last
fruits.sort()                  # Sort in-place
fruits.reverse()               # Reverse in-place

# Slicing
nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print(nums[2:5])    # [2, 3, 4]
print(nums[::2])    # [0, 2, 4, 6, 8]   -- step of 2
print(nums[::-1])   # [9, 8, 7, ..., 0]  -- reverse
print(nums[-3:])    # [7, 8, 9]          -- last 3

# Copying (shallow vs reference)
a = [1, 2, 3]
b = a        # reference -- same object
c = a[:]     # shallow copy
d = a.copy() # shallow copy
```

---

## 2. Tuples

```python
# Tuples are IMMUTABLE
point = (3, 4)
rgb = (255, 128, 0)
singleton = (42,)  # Note the comma!

# Packing & Unpacking
x, y = point
name, age, city = ("Alice", 30, "Bangalore")

# Swap using unpacking
a, b = 10, 20
a, b = b, a  # a=20, b=10

# Extended unpacking
first, *rest = [1, 2, 3, 4, 5]
# first = 1, rest = [2, 3, 4, 5]

# Tuples as dict keys (since they're hashable)
locations = {(28.6, 77.2): "Delhi", (13.0, 80.2): "Chennai"}
```

---

## 3. Dictionaries

```python
# Creation
student = {"name": "Alice", "age": 25, "grade": "A"}
empty = {}
from_keys = dict.fromkeys(["a", "b", "c"], 0)

# Access
name = student["name"]           # KeyError if missing
age = student.get("age", 0)      # Default if missing

# Methods
student.update({"grade": "A+", "city": "Mumbai"})
keys = student.keys()
values = student.values()
items = student.items()
removed = student.pop("city", None)

# Iteration
for key, value in student.items():
    print(f"{key}: {value}")

# Nested Dictionaries
company = {
    "engineering": {"head": "Alice", "size": 50},
    "sales": {"head": "Bob", "size": 30},
}
print(company["engineering"]["head"])  # Alice
```

---

## 4. Sets

```python
# Creation
s = {1, 2, 3, 4, 5}
empty_set = set()  # NOT {} -- that's a dict!

# Operations
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

print(a | b)   # Union:        {1, 2, 3, 4, 5, 6}
print(a & b)   # Intersection: {3, 4}
print(a - b)   # Difference:   {1, 2}
print(a ^ b)   # Symmetric:    {1, 2, 5, 6}

# Methods
s.add(6)
s.discard(3)     # No error if missing
s.remove(2)      # KeyError if missing

# Frozen Set (immutable)
fs = frozenset([1, 2, 3])
# fs.add(4)  # AttributeError -- frozen!
```

---

## 5. Comprehensions

```python
# List Comprehension
squares = [x**2 for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]

# Dict Comprehension
word_lengths = {w: len(w) for w in ["hello", "world", "python"]}
# {'hello': 5, 'world': 5, 'python': 6}

# Set Comprehension
unique_lengths = {len(w) for w in ["hi", "hello", "hey", "hola"]}
# {2, 3, 4, 5}

# Nested Comprehension
matrix = [[i * j for j in range(1, 4)] for i in range(1, 4)]
# [[1,2,3], [2,4,6], [3,6,9]]

# Flatten nested list
flat = [x for row in matrix for x in row]

# Conditional expression in comprehension
labels = ["even" if x % 2 == 0 else "odd" for x in range(6)]
```

---

## 6. enumerate() and zip()

```python
# enumerate -- index + value
fruits = ["apple", "banana", "cherry"]
for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")

for i, fruit in enumerate(fruits, start=1):  # Custom start
    print(f"{i}. {fruit}")

# zip -- parallel iteration
names = ["Alice", "Bob", "Charlie"]
scores = [88, 95, 72]
for name, score in zip(names, scores):
    print(f"{name}: {score}")

# zip to create dict
name_score_dict = dict(zip(names, scores))

# zip with unequal lengths -- stops at shortest
# Use itertools.zip_longest for longest
```

---

## 7. Collections Module

```python
from collections import Counter, defaultdict, deque, OrderedDict

# Counter -- frequency counting
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
count = Counter(words)
print(count)                # Counter({'apple': 3, 'banana': 2, 'cherry': 1})
print(count.most_common(2)) # [('apple', 3), ('banana', 2)]

# defaultdict -- auto-initialize missing keys
dd = defaultdict(list)
data = [("fruits", "apple"), ("vegs", "carrot"), ("fruits", "banana")]
for category, item in data:
    dd[category].append(item)
# {'fruits': ['apple', 'banana'], 'vegs': ['carrot']}

# deque -- double-ended queue (O(1) append/pop from both ends)
dq = deque([1, 2, 3])
dq.appendleft(0)   # [0, 1, 2, 3]
dq.append(4)        # [0, 1, 2, 3, 4]
dq.popleft()         # removes 0
dq.rotate(2)         # rotate right by 2

# OrderedDict (Python 3.7+ dicts are ordered, but OrderedDict has extra methods)
od = OrderedDict()
od["first"] = 1
od["second"] = 2
od.move_to_end("first")  # Move to end
```

---

## 8. Iterators & Iterables

```python
# Iterable: any object with __iter__() method
# Iterator: any object with __next__() method

my_list = [1, 2, 3]          # Iterable
my_iter = iter(my_list)       # Iterator

print(next(my_iter))  # 1
print(next(my_iter))  # 2
print(next(my_iter))  # 3
# next(my_iter)       # StopIteration!

# Custom Iterator
class Countdown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value

for num in Countdown(5):
    print(num, end=" ")  # 5 4 3 2 1
```

---

##  Interview Tips
- Know the **time complexity** of common operations (list append O(1), insert O(n), dict lookup O(1))
- **Counter** is your best friend for frequency problems
- **defaultdict** eliminates key-existence checks
- **deque** is ideal for BFS, sliding window problems
- Comprehensions are more Pythonic than map/filter for simple cases
- Understand shallow vs deep copy (`copy.deepcopy()`)

##  Practice Problems
| Problem | Platform | Difficulty |
|---------|----------|------------|
| Group Anagrams | LeetCode 49 | Medium |
| Contains Duplicate | LeetCode 217 | Easy |
| Majority Element | LeetCode 169 | Easy |
| Lists | HackerRank | Easy |
| Nested Lists | HackerRank | Easy |
