# Day 8 -- File Handling & Data Processing 

Welcome to Day 8! Today we dive into one of the most practical and essential skills in
programming -- **File Handling and Data Processing**. Whether you're building data pipelines,
processing logs, or working with APIs, mastering file I/O is non-negotiable.

---

## Table of Contents

1. [Reading & Writing Files](#1-reading--writing-files)
2. [The `with` Statement (Context Managers)](#2-the-with-statement-context-managers)
3. [CSV Library](#3-csv-library)
4. [JSON Handling](#4-json-handling)
5. [XML Basics](#5-xml-basics)
6. [Log File Parsing](#6-log-file-parsing)
7. [Data Serialization](#7-data-serialization)
8. [File Path Handling](#8-file-path-handling)
9. [Practice Exercises](#9-practice-exercises)
10. [LeetCode Problems](#10-leetcode-problems)
11. [Corporate Use Case](#11-corporate-use-case)

---

## 1. Reading & Writing Files

Python provides the built-in `open()` function to interact with files. Understanding
file modes is critical for correct file operations.

### File Modes

| Mode | Description                                      |
|------|--------------------------------------------------|
| `r`  | Read (default). File must exist.                 |
| `w`  | Write. Creates file or **truncates** existing.   |
| `a`  | Append. Creates file if it doesn't exist.        |
| `x`  | Exclusive creation. Fails if file exists.        |
| `rb` | Read binary (images, PDFs, etc.).                |
| `wb` | Write binary.                                    |
| `r+` | Read and write (file must exist).                |
| `w+` | Write and read (truncates existing).             |
| `a+` | Append and read.                                 |

### Reading Files

```python
# Method 1: read() -- reads the ENTIRE file into a single string
file = open("example.txt", "r")
content = file.read()
print(content)
file.close()  # Always close the file!

# Method 2: readline() -- reads ONE line at a time
file = open("example.txt", "r")
first_line = file.readline()   # "Hello World\n"
second_line = file.readline()  # "This is line 2\n"
file.close()

# Method 3: readlines() -- reads ALL lines into a list
file = open("example.txt", "r")
lines = file.readlines()  # ["Hello World\n", "This is line 2\n", ...]
file.close()

# Method 4: Iterate line by line (memory efficient for large files)
file = open("example.txt", "r")
for line in file:
    print(line.strip())  # strip() removes trailing newline
file.close()
```

### Writing Files

```python
# Write mode -- creates or OVERWRITES existing content
file = open("output.txt", "w")
file.write("First line of output\n")
file.write("Second line of output\n")
file.close()

# writelines() -- writes a list of strings (no newlines added automatically)
lines = ["Line 1\n", "Line 2\n", "Line 3\n"]
file = open("output.txt", "w")
file.writelines(lines)
file.close()
```

### Append Mode

```python
# Append mode -- adds to the END of the file without overwriting
file = open("output.txt", "a")
file.write("This line is appended\n")
file.close()
```

### Binary Mode

```python
# Reading a binary file (e.g., an image)
with open("photo.jpg", "rb") as f:
    binary_data = f.read()
    print(f"File size: {len(binary_data)} bytes")

# Writing binary data
with open("copy_photo.jpg", "wb") as f:
    f.write(binary_data)
```

>  **Common Pitfall**: Forgetting to call `file.close()` can lead to data loss
> or resource leaks. The `with` statement (next section) solves this elegantly.

---

## 2. The `with` Statement (Context Managers)

The `with` statement is the **Pythonic** way to handle files. It automatically closes
the file when the block exits -- even if an exception occurs.

### Basic Usage

```python
# The file is automatically closed after the block
with open("example.txt", "r") as file:
    content = file.read()
    print(content)
# No need to call file.close() -- it's handled automatically!
```

### Why Use `with`?

```python
# WITHOUT with -- risky if an error occurs between open and close
file = open("data.txt", "r")
try:
    data = file.read()
    process(data)  # What if this raises an error?
finally:
    file.close()   # This ensures close happens, but it's verbose

# WITH with -- clean, safe, and Pythonic
with open("data.txt", "r") as file:
    data = file.read()
    process(data)
# File is closed automatically, even if process() raises an error
```

### Multiple Files

```python
# Open multiple files simultaneously
with open("input.txt", "r") as infile, open("output.txt", "w") as outfile:
    for line in infile:
        outfile.write(line.upper())
```

### How It Works -- The Context Manager Protocol

Any object that implements `__enter__()` and `__exit__()` methods can be used
with the `with` statement:

```python
class FileManager:
    """Custom context manager example."""

    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
        return False  # Don't suppress exceptions


# Usage
with FileManager("test.txt", "w") as f:
    f.write("Hello from custom context manager!\n")
```

---

## 3. CSV Library

CSV (Comma-Separated Values) is one of the most common data exchange formats.
Python's built-in `csv` module handles all the edge cases (quoted fields, commas
within values, different delimiters, etc.).

### csv.reader -- Reading CSV Files

```python
import csv

# Basic CSV reading
with open("employees.csv", "r", newline="") as file:
    reader = csv.reader(file)
    header = next(reader)  # Skip the header row
    print(f"Columns: {header}")

    for row in reader:
        # Each row is a list of strings
        print(f"Name: {row[1]}, Department: {row[2]}, Salary: {row[3]}")
```

### csv.writer -- Writing CSV Files

```python
import csv

# Writing CSV data
data = [
    ["id", "name", "department", "salary"],
    [1, "Alice", "Engineering", 95000],
    [2, "Bob", "Marketing", 72000],
    [3, "Charlie", "Engineering", 88000],
]

with open("output.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(data)  # Write all rows at once
    # Or write one row at a time:
    # for row in data:
    #     writer.writerow(row)
```

### csv.DictReader -- Reading as Dictionaries

```python
import csv

# Each row becomes an OrderedDict with column headers as keys
with open("employees.csv", "r", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        # Access fields by column name -- much more readable!
        print(f"{row['name']} works in {row['department']}")
        print(f"  Salary: ${row['salary']}")
```

### csv.DictWriter -- Writing from Dictionaries

```python
import csv

fieldnames = ["id", "name", "department", "salary"]
employees = [
    {"id": 1, "name": "Alice", "department": "Engineering", "salary": 95000},
    {"id": 2, "name": "Bob", "department": "Marketing", "salary": 72000},
]

with open("output.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()        # Write the header row
    writer.writerows(employees) # Write all data rows
```

### Custom Delimiters

```python
import csv

# Reading a TSV (Tab-Separated Values) file
with open("data.tsv", "r", newline="") as file:
    reader = csv.reader(file, delimiter="\t")
    for row in reader:
        print(row)

# Using pipe as a delimiter
with open("data.txt", "r", newline="") as file:
    reader = csv.reader(file, delimiter="|")
    for row in reader:
        print(row)
```

>  **Tip**: Always use `newline=""` when opening CSV files to prevent issues with
> line endings on different operating systems.

---

## 4. JSON Handling

JSON (JavaScript Object Notation) is the **lingua franca** of web APIs and
configuration files. Python's `json` module provides seamless conversion between
JSON strings and Python objects.

### JSON  Python Type Mapping

| JSON Type   | Python Type |
|-------------|-------------|
| `object`    | `dict`      |
| `array`     | `list`      |
| `string`    | `str`       |
| `number`    | `int/float` |
| `true/false`| `True/False`|
| `null`      | `None`      |

### json.load -- Read JSON from a File

```python
import json

# Load JSON data from a file
with open("config.json", "r") as file:
    config = json.load(file)

print(config["database"]["host"])   # Access nested data
print(config["database"]["port"])
```

### json.dump -- Write JSON to a File

```python
import json

data = {
    "name": "Alice",
    "age": 30,
    "skills": ["Python", "SQL", "Machine Learning"],
    "address": {
        "city": "Bangalore",
        "state": "Karnataka"
    }
}

# Write JSON to a file with pretty printing
with open("output.json", "w") as file:
    json.dump(data, file, indent=4, sort_keys=True)
```

### json.loads -- Parse JSON String

```python
import json

# Parse a JSON string into a Python object
json_string = '{"name": "Bob", "age": 25, "active": true}'
data = json.loads(json_string)

print(data["name"])    # "Bob"
print(data["active"])  # True (Python bool)
print(type(data))      # <class 'dict'>
```

### json.dumps -- Convert Python Object to JSON String

```python
import json

data = {"name": "Charlie", "scores": [95, 87, 92], "graduated": False}

# Convert to JSON string
json_string = json.dumps(data)
print(json_string)
# '{"name": "Charlie", "scores": [95, 87, 92], "graduated": false}'

# Pretty print with indentation
pretty_json = json.dumps(data, indent=2, sort_keys=True)
print(pretty_json)
```

### Pretty Printing

```python
import json

complex_data = {
    "company": "TechCorp",
    "employees": [
        {"name": "Alice", "role": "Engineer", "projects": ["Alpha", "Beta"]},
        {"name": "Bob", "role": "Designer", "projects": ["Gamma"]},
    ],
    "founded": 2015,
    "active": True
}

# Pretty print to console
print(json.dumps(complex_data, indent=4, sort_keys=True))

# Pretty print to file
with open("company.json", "w") as f:
    json.dump(complex_data, f, indent=4, sort_keys=True)
```

### Handling Special Cases

```python
import json
from datetime import datetime

# Custom encoder for non-serializable types
class CustomEncoder(json.JSONEncoder):
    """Handle datetime and set objects in JSON serialization."""

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, set):
            return list(obj)
        return super().default(obj)


data = {
    "timestamp": datetime.now(),
    "tags": {"python", "json", "tutorial"}
}

json_str = json.dumps(data, cls=CustomEncoder, indent=2)
print(json_str)
```

---

## 5. XML Basics

XML (eXtensible Markup Language) is used in many enterprise systems, configuration
files (like Maven's `pom.xml`), and SOAP APIs. Python's `xml.etree.ElementTree`
module provides a simple and efficient way to parse XML.

### Parsing XML from a String

```python
import xml.etree.ElementTree as ET

xml_data = """<?xml version="1.0"?>
<catalog>
    <book id="1">
        <title>Python Crash Course</title>
        <author>Eric Matthes</author>
        <price>29.99</price>
    </book>
    <book id="2">
        <title>Automate the Boring Stuff</title>
        <author>Al Sweigart</author>
        <price>24.99</price>
    </book>
</catalog>"""

# Parse the XML string
root = ET.fromstring(xml_data)

# Iterate over all book elements
for book in root.findall("book"):
    book_id = book.get("id")                  # Get attribute
    title = book.find("title").text            # Get child element text
    author = book.find("author").text
    price = float(book.find("price").text)
    print(f"[{book_id}] {title} by {author} -- ${price:.2f}")
```

### Parsing XML from a File

```python
import xml.etree.ElementTree as ET

# Parse an XML file
tree = ET.parse("catalog.xml")
root = tree.getroot()

print(f"Root tag: {root.tag}")         # 'catalog'
print(f"Root attributes: {root.attrib}")

# Find all elements with a specific tag
for book in root.iter("book"):
    print(book.find("title").text)
```

### Creating XML

```python
import xml.etree.ElementTree as ET

# Build XML structure programmatically
root = ET.Element("employees")

emp1 = ET.SubElement(root, "employee", id="101")
ET.SubElement(emp1, "name").text = "Alice"
ET.SubElement(emp1, "department").text = "Engineering"
ET.SubElement(emp1, "salary").text = "95000"

emp2 = ET.SubElement(root, "employee", id="102")
ET.SubElement(emp2, "name").text = "Bob"
ET.SubElement(emp2, "department").text = "Marketing"
ET.SubElement(emp2, "salary").text = "72000"

# Write to file
tree = ET.ElementTree(root)
ET.indent(tree, space="    ")  # Pretty print (Python 3.9+)
tree.write("employees.xml", encoding="unicode", xml_declaration=True)
```

### XPath-style Searching

```python
import xml.etree.ElementTree as ET

xml_data = """<store>
    <department name="Electronics">
        <product><name>Laptop</name><price>999</price></product>
        <product><name>Phone</name><price>699</price></product>
    </department>
    <department name="Books">
        <product><name>Python Guide</name><price>39</price></product>
    </department>
</store>"""

root = ET.fromstring(xml_data)

# Find all products across all departments
for product in root.findall(".//product"):
    name = product.find("name").text
    price = product.find("price").text
    print(f"{name}: ${price}")

# Find products in a specific department
for dept in root.findall("department[@name='Electronics']"):
    for product in dept.findall("product"):
        print(f"Electronics: {product.find('name').text}")
```

---

## 6. Log File Parsing

Log file analysis is a critical skill for debugging, monitoring, and security
auditing. Here's how to parse and analyze structured log files.

### Parsing Apache-style Logs

```python
import re
from collections import Counter

# Sample log entries
log_data = """
192.168.1.10 - - [15/May/2025:10:15:30 +0530] "GET /index.html HTTP/1.1" 200 1234
192.168.1.11 - - [15/May/2025:10:15:31 +0530] "POST /api/login HTTP/1.1" 401 89
192.168.1.10 - - [15/May/2025:10:15:32 +0530] "GET /dashboard HTTP/1.1" 200 5678
192.168.1.12 - - [15/May/2025:10:15:33 +0530] "GET /admin HTTP/1.1" 403 45
192.168.1.11 - - [15/May/2025:10:15:34 +0530] "POST /api/login HTTP/1.1" 401 89
""".strip()

# Regex pattern for Apache combined log format
pattern = r'(\S+) - - \[(.+?)\] "(\S+) (\S+) (\S+)" (\d+) (\d+)'

status_codes = Counter()
ip_addresses = Counter()
failed_requests = []

for line in log_data.split("\n"):
    match = re.match(pattern, line)
    if match:
        ip, timestamp, method, path, protocol, status, size = match.groups()
        status_codes[status] += 1
        ip_addresses[ip] += 1

        if int(status) >= 400:
            failed_requests.append({
                "ip": ip, "path": path,
                "status": status, "time": timestamp
            })

print("=== Status Code Summary ===")
for code, count in status_codes.most_common():
    print(f"  {code}: {count} requests")

print("\n=== Top IPs ===")
for ip, count in ip_addresses.most_common(5):
    print(f"  {ip}: {count} requests")

print("\n=== Failed Requests ===")
for req in failed_requests:
    print(f"  [{req['status']}] {req['ip']} -> {req['path']}")
```

### Parsing Application Logs with Timestamps

```python
from datetime import datetime
from collections import defaultdict

log_lines = [
    "2025-05-15 10:30:01 ERROR Database connection timeout",
    "2025-05-15 10:30:05 INFO  Retrying connection...",
    "2025-05-15 10:30:10 ERROR Database connection timeout",
    "2025-05-15 10:31:00 INFO  Connection established",
    "2025-05-15 11:00:00 WARN  High memory usage: 85%",
    "2025-05-15 11:05:00 ERROR Out of memory exception",
]

# Categorize by log level
logs_by_level = defaultdict(list)

for line in log_lines:
    parts = line.split(maxsplit=3)
    date_str = f"{parts[0]} {parts[1]}"
    level = parts[2].strip()
    message = parts[3] if len(parts) > 3 else ""

    timestamp = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    logs_by_level[level].append({"time": timestamp, "message": message})

for level, entries in logs_by_level.items():
    print(f"\n[{level}] -- {len(entries)} entries")
    for entry in entries:
        print(f"  {entry['time'].strftime('%H:%M:%S')} | {entry['message']}")
```

---

## 7. Data Serialization

Serialization is the process of converting Python objects into a format that can
be stored or transmitted, and later reconstructed.

### Pickle -- Python's Native Serialization

```python
import pickle

# Serialize (dump) Python objects
data = {
    "model": "RandomForest",
    "accuracy": 0.95,
    "features": ["age", "income", "score"],
    "trained": True
}

# Save to a file
with open("model_data.pkl", "wb") as f:
    pickle.dump(data, f)

# Load from a file
with open("model_data.pkl", "rb") as f:
    loaded_data = pickle.load(f)

print(loaded_data)
print(loaded_data["accuracy"])  # 0.95
```

### Pickle with Complex Objects

```python
import pickle

class Employee:
    """Example class for serialization."""

    def __init__(self, name, department, salary):
        self.name = name
        self.department = department
        self.salary = salary

    def __repr__(self):
        return f"Employee({self.name}, {self.department}, ${self.salary})"


employees = [
    Employee("Alice", "Engineering", 95000),
    Employee("Bob", "Marketing", 72000),
]

# Serialize
with open("employees.pkl", "wb") as f:
    pickle.dump(employees, f)

# Deserialize
with open("employees.pkl", "rb") as f:
    loaded = pickle.load(f)

for emp in loaded:
    print(emp)  # Employee(Alice, Engineering, $95000)
```

### JSON vs Pickle -- When to Use What

| Feature              | JSON                          | Pickle                          |
|----------------------|-------------------------------|---------------------------------|
| **Human Readable**   |  Yes                        |  No (binary)                  |
| **Language Support** |  Universal                  |  Python only                  |
| **Security**         |  Safe                       |  Unsafe (arbitrary code exec)|
| **Data Types**       | Limited (str, int, list, dict)| All Python objects              |
| **Speed**            | Moderate                      | Fast                            |
| **File Size**        | Larger (text)                 | Smaller (binary)                |
| **Use Case**         | APIs, configs, data exchange  | ML models, caching, internal    |

```python
import json
import pickle

data = {"name": "Alice", "scores": [95, 87, 92]}

# JSON -- human readable, cross-language
json_str = json.dumps(data, indent=2)
print(f"JSON ({len(json_str)} chars):\n{json_str}")

# Pickle -- compact, Python-specific
pickle_bytes = pickle.dumps(data)
print(f"\nPickle ({len(pickle_bytes)} bytes): {pickle_bytes[:50]}...")
```

>  **Security Warning**: Never `pickle.load()` data from untrusted sources!
> Pickle can execute arbitrary code during deserialization, making it a potential
> security vulnerability.

---

## 8. File Path Handling

Python offers two approaches for working with file paths: the traditional `os.path`
module and the modern `pathlib` module (recommended for new code).

### os.path -- Traditional Approach

```python
import os

# Join paths (OS-independent)
path = os.path.join("data", "2025", "sales.csv")
print(path)  # data/2025/sales.csv (or data\2025\sales.csv on Windows)

# Get file information
filepath = "/home/user/documents/report.pdf"
print(os.path.basename(filepath))   # report.pdf
print(os.path.dirname(filepath))    # /home/user/documents
print(os.path.splitext(filepath))   # ('/home/user/documents/report', '.pdf')
print(os.path.exists(filepath))     # True/False
print(os.path.isfile(filepath))     # True if it's a file
print(os.path.isdir(filepath))      # True if it's a directory
print(os.path.getsize(filepath))    # File size in bytes

# Get absolute path
rel_path = "data/file.txt"
abs_path = os.path.abspath(rel_path)
print(abs_path)

# List directory contents
for item in os.listdir("."):
    full_path = os.path.join(".", item)
    if os.path.isfile(full_path):
        size = os.path.getsize(full_path)
        print(f"  FILE: {item} ({size} bytes)")
    else:
        print(f"  DIR:  {item}/")
```

### pathlib -- Modern Approach (Recommended)

```python
from pathlib import Path

# Create path objects
p = Path("data") / "2025" / "sales.csv"
print(p)  # data/2025/sales.csv

# Path properties
filepath = Path("/home/user/documents/report.pdf")
print(filepath.name)       # report.pdf
print(filepath.stem)       # report
print(filepath.suffix)     # .pdf
print(filepath.parent)     # /home/user/documents
print(filepath.parts)      # ('/', 'home', 'user', 'documents', 'report.pdf')

# Check existence
print(filepath.exists())   # True/False
print(filepath.is_file())  # True if it's a file
print(filepath.is_dir())   # True if it's a directory

# Read and write (convenience methods!)
p = Path("example.txt")
p.write_text("Hello, pathlib!\nSecond line.\n")
content = p.read_text()
print(content)

# Binary read/write
binary_path = Path("data.bin")
binary_path.write_bytes(b"\x00\x01\x02\x03")
data = binary_path.read_bytes()

# Create directories
Path("output/reports/2025").mkdir(parents=True, exist_ok=True)

# Glob -- find files matching a pattern
for py_file in Path(".").glob("**/*.py"):
    print(f"Python file: {py_file}")

# Iterating directory contents
for item in Path(".").iterdir():
    kind = "DIR" if item.is_dir() else "FILE"
    print(f"  [{kind}] {item.name}")
```

### Practical Example: Organizing Files

```python
from pathlib import Path
import shutil

def organize_by_extension(source_dir):
    """Organize files in a directory into subdirectories by extension."""
    source = Path(source_dir)

    for file_path in source.iterdir():
        if file_path.is_file():
            # Get extension without dot, default to 'no_extension'
            ext = file_path.suffix.lstrip(".") or "no_extension"

            # Create target directory
            target_dir = source / ext
            target_dir.mkdir(exist_ok=True)

            # Move file
            target = target_dir / file_path.name
            shutil.move(str(file_path), str(target))
            print(f"Moved: {file_path.name} -> {ext}/")


# Usage: organize_by_extension("Downloads")
```

---

## 9. Practice Exercises

Check out the `practice/` directory for hands-on exercises:

| File                    | Description                                      |
|-------------------------|--------------------------------------------------|
| `file_operations.py`    | Read/write text files, append mode, binary files |
| `csv_json_handling.py`  | CSV & JSON reading, writing, and conversion      |
| `sample_data.csv`       | Sample employee dataset (CSV format)             |
| `sample_data.json`      | Sample employee dataset (JSON format)            |

---

## 10. LeetCode Problems

Today's problems focus on matrix manipulation, which pairs well with our data
processing theme:

| #  | Problem                          | Difficulty | Key Concept                |
|----|----------------------------------|------------|----------------------------|
| 36 | Valid Sudoku                     | Medium     | Sets, 2D array validation  |
| 1572 | Matrix Diagonal Sum           | Easy       | Matrix traversal           |

Find solutions in the `official_questions/` directory.

---

## 11. Corporate Use Case

### Security Audit Log Analyzer

The `Corporate_use_case/security_audit_log_analyzer.py` demonstrates a real-world
application combining multiple file handling concepts:

- **Log parsing** with structured data
- **CSV output** for reports
- **JSON export** for API consumption
- **datetime** handling for temporal analysis
- **Threat level** classification

This tool analyzes security logs to detect:
-  Brute force attempts (repeated failed logins)
-  Suspicious IP activity
-  After-hours access patterns
-  Normal activity baseline

---

## Quick Reference Card

```python
# === FILE I/O ===
with open("file.txt", "r") as f:    # Read
    content = f.read()
with open("file.txt", "w") as f:    # Write (overwrite)
    f.write("data")
with open("file.txt", "a") as f:    # Append
    f.write("more data")

# === CSV ===
import csv
reader = csv.DictReader(open("data.csv"))
writer = csv.DictWriter(open("out.csv", "w"), fieldnames=["a", "b"])

# === JSON ===
import json
data = json.load(open("data.json"))           # File -> Python
json.dump(data, open("out.json", "w"))        # Python -> File
data = json.loads('{"key": "value"}')         # String -> Python
s = json.dumps(data, indent=2)               # Python -> String

# === PATHS ===
from pathlib import Path
p = Path("dir") / "subdir" / "file.txt"
p.read_text()  /  p.write_text("content")
p.exists()  /  p.is_file()  /  p.is_dir()
list(p.parent.glob("*.py"))
```

---

## Key Takeaways

1. **Always use `with` statements** for file operations -- it's safer and cleaner.
2. **Use `csv.DictReader`/`DictWriter`** for readable CSV code.
3. **`json.dumps(data, indent=4)`** for pretty-printed, debuggable JSON.
4. **Prefer `pathlib.Path`** over `os.path` for new code -- it's more intuitive.
5. **Never unpickle untrusted data** -- it's a security risk.
6. **Use `newline=""`** when opening CSV files to avoid line ending issues.
7. **Binary mode (`rb`/`wb`)** is essential for non-text files (images, PDFs, etc.).

---

*Happy coding!  File handling is where theory meets real-world programming.*
