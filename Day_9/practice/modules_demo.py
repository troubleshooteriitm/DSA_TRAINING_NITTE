"""
Day 9 Practice -- Modules Demo

This script demonstrates:
    1. Creating and using modules
    2. Different import styles
    3. The __name__ == '__main__' guard
    4. Package structure concepts
    5. Useful built-in modules
    6. Module inspection utilities

Note: This file is self-contained. It simulates module behavior
      by dynamically creating temporary module files for demonstration.
"""

import sys
import os
import importlib
import tempfile
import math
import json
import datetime


# ============================================================================
# Section 1: Understanding __name__
# ============================================================================
def demo_name_variable():
    """
    Demonstrate how __name__ works.

    When a file is run directly:  __name__ == '__main__'
    When a file is imported:      __name__ == '<module_name>'
    """
    print("=" * 60)
    print("SECTION 1: The __name__ Variable")
    print("=" * 60)

    print(f"\nCurrent file's __name__: {__name__}")
    print(f"   This is '__main__' because we're running this file directly.")

    # Check __name__ of imported modules
    print(f"\nImported 'math' module's __name__: {math.__name__}")
    print(f"Imported 'json' module's __name__: {json.__name__}")
    print(f"Imported 'os' module's __name__:   {os.__name__}")

    print("\n Key Takeaway:")
    print("   Use `if __name__ == '__main__':` to write code that runs")
    print("   ONLY when the file is executed directly, not when imported.")
    print()


# ============================================================================
# Section 2: Creating and Importing Modules Dynamically
# ============================================================================
def demo_creating_modules():
    """
    Create a temporary Python module file and import it dynamically.

    This demonstrates the full lifecycle:
        1. Write a .py file (creating a module)
        2. Add its directory to sys.path
        3. Import it
        4. Use its functions and variables
    """
    print("=" * 60)
    print("SECTION 2: Creating and Importing Modules")
    print("=" * 60)

    # --- Step 1: Create a temporary module file ---
    module_code = '''
"""A sample math utilities module."""

PI = 3.14159265358979
E = 2.71828182845905

def add(a, b):
    """Return the sum of two numbers."""
    return a + b

def multiply(a, b):
    """Return the product of two numbers."""
    return a * b

def circle_area(radius):
    """Calculate area of a circle."""
    return PI * radius ** 2

def factorial(n):
    """Calculate factorial recursively."""
    if n <= 1:
        return 1
    return n * factorial(n - 1)

# This runs ONLY when math_helpers.py is executed directly
if __name__ == "__main__":
    print("Running math_helpers as a standalone script!")
    print(f"circle_area(5) = {circle_area(5)}")
'''

    # Create a temporary directory and write the module file
    temp_dir = tempfile.mkdtemp(prefix="pymodule_demo_")
    module_path = os.path.join(temp_dir, "math_helpers.py")

    with open(module_path, "w") as f:
        f.write(module_code)

    print(f"\n Created module file: {module_path}")

    # --- Step 2: Add directory to sys.path ---
    sys.path.insert(0, temp_dir)
    print(f" Added '{temp_dir}' to sys.path")

    # --- Step 3: Import the module ---
    import math_helpers  # noqa: E402 -- dynamic import

    print(f" Imported 'math_helpers' module")
    print(f"   Module file: {math_helpers.__file__}")
    print(f"   Module name: {math_helpers.__name__}")

    # --- Step 4: Use the module ---
    print(f"\n--- Using math_helpers ---")
    print(f"   math_helpers.PI          = {math_helpers.PI}")
    print(f"   math_helpers.add(10, 20) = {math_helpers.add(10, 20)}")
    print(f"   math_helpers.multiply(3, 7) = {math_helpers.multiply(3, 7)}")
    print(f"   math_helpers.circle_area(5) = {math_helpers.circle_area(5):.4f}")
    print(f"   math_helpers.factorial(6)   = {math_helpers.factorial(6)}")

    # --- Step 5: Different import styles (simulated) ---
    print(f"\n--- Import Styles ---")
    print(f"   'import math_helpers'             Access via math_helpers.add()")
    print(f"   'from math_helpers import add'    Access directly via add()")
    print(f"   'import math_helpers as mh'       Access via mh.add()")
    print(f"   'from math_helpers import *'      All names available (avoid!)")

    # --- Cleanup ---
    # Remove from sys.path and sys.modules
    sys.path.remove(temp_dir)
    del sys.modules["math_helpers"]
    os.remove(module_path)
    os.rmdir(temp_dir)
    print(f"\n Cleaned up temporary module files.")
    print()


# ============================================================================
# Section 3: Exploring sys.path -- How Python Finds Modules
# ============================================================================
def demo_sys_path():
    """
    Show the directories Python searches when importing modules.
    """
    print("=" * 60)
    print("SECTION 3: sys.path -- Module Search Paths")
    print("=" * 60)

    print(f"\nPython searches these directories (in order) when importing:\n")
    for i, path in enumerate(sys.path):
        label = ""
        if i == 0:
            label = "  (script directory or '')"
        elif "site-packages" in path:
            label = "  (third-party packages)"
        elif "lib" in path.lower() and "python" in path.lower():
            label = "  (standard library)"
        print(f"  [{i:2d}] {path}{label}")

    print(f"\n You can modify sys.path to add custom module directories:")
    print(f"   sys.path.append(r'D:\\my_custom_libs')")
    print(f"   sys.path.insert(0, '/home/user/my_libs')  # Higher priority")
    print()


# ============================================================================
# Section 4: Module Inspection
# ============================================================================
def demo_module_inspection():
    """
    Demonstrate how to inspect modules -- their attributes, source file,
    documentation, etc.
    """
    print("=" * 60)
    print("SECTION 4: Module Inspection")
    print("=" * 60)

    # Inspect the 'json' module
    print(f"\n--- Inspecting 'json' module ---")
    print(f"   File:    {json.__file__}")
    print(f"   Name:    {json.__name__}")
    print(f"   Package: {json.__package__}")
    print(f"   Doc:     {json.__doc__[:80]}...")

    # List public attributes
    public_attrs = [attr for attr in dir(json) if not attr.startswith("_")]
    print(f"\n   Public attributes ({len(public_attrs)}):")
    for i in range(0, len(public_attrs), 5):
        chunk = public_attrs[i:i + 5]
        print(f"      {', '.join(chunk)}")

    # Inspect the 'os' module
    print(f"\n--- Inspecting 'os' module ---")
    print(f"   File:    {os.__file__}")
    print(f"   Name:    {os.__name__}")
    print(f"   Some useful functions:")

    useful_os_funcs = [
        "os.getcwd()",
        "os.listdir('.')",
        "os.path.exists('file.txt')",
        "os.path.join('dir', 'file.txt')",
        "os.makedirs('a/b/c', exist_ok=True)",
    ]
    for func in useful_os_funcs:
        print(f"      {func}")

    print()


# ============================================================================
# Section 5: Package Structure Explanation
# ============================================================================
def demo_package_structure():
    """
    Explain and visualize Python package structure.
    """
    print("=" * 60)
    print("SECTION 5: Package Structure")
    print("=" * 60)

    package_tree = """
    A Python PACKAGE is a directory containing an __init__.py file
    and one or more modules (.py files).

    Example project structure:
    
      my_project/                                            
       main.py               Entry point                
       config.py             Top-level module           
                                                            
       utils/                Package                    
          __init__.py       Package initializer        
          string_ops.py     Module                     
          math_ops.py       Module                     
          validators.py     Module                     
                                                            
       database/             Package                    
          __init__.py       Package initializer        
          connection.py     Module                     
          models.py         Module                     
          queries.py        Module                     
                                                            
       tests/                Package                    
           __init__.py                                    
           test_utils.py                                  
           test_database.py                               
    
    """
    print(package_tree)

    print("  --- __init__.py Examples ---\n")

    init_example = '''
    # utils/__init__.py

    # 1. Empty __init__.py -- just marks directory as a package
    #    (This is the minimum requirement)

    # 2. Import shortcuts -- so users can write 'from utils import add'
    #    instead of 'from utils.math_ops import add'
    from .math_ops import add, multiply
    from .string_ops import capitalize

    # 3. Package-level variables
    __version__ = "1.0.0"
    __author__ = "Your Name"

    # 4. Control what 'from utils import *' exports
    __all__ = ['add', 'multiply', 'capitalize']
    '''
    print(init_example)

    print("  --- Import Examples from the Structure Above ---\n")
    import_examples = [
        ("import utils.math_ops",
         "utils.math_ops.add(1, 2)"),
        ("from utils import math_ops",
         "math_ops.add(1, 2)"),
        ("from utils.math_ops import add",
         "add(1, 2)"),
        ("from utils.math_ops import add as plus",
         "plus(1, 2)"),
    ]

    print(f"    {'Import Statement':<45} {'Usage'}")
    print(f"    {'-' * 45} {'-' * 25}")
    for imp, usage in import_examples:
        print(f"    {imp:<45} {usage}")

    print(f"\n  --- Relative vs Absolute Imports ---\n")
    print(f"    ABSOLUTE (recommended for clarity):")
    print(f"      from utils.math_ops import add")
    print(f"      from database.connection import connect")
    print()
    print(f"    RELATIVE (within a package):")
    print(f"      from . import math_ops          # Same package")
    print(f"      from .math_ops import add        # Same package, specific item")
    print(f"      from .. import config            # Parent package")
    print(f"      from ..database import models    # Sibling package")
    print()


# ============================================================================
# Section 6: Useful Built-in Modules Showcase
# ============================================================================
def demo_builtin_modules():
    """
    Showcase some commonly used built-in Python modules.
    """
    print("=" * 60)
    print("SECTION 6: Useful Built-in Modules")
    print("=" * 60)

    # --- math module ---
    print(f"\n   math module:")
    print(f"     math.pi       = {math.pi}")
    print(f"     math.e        = {math.e}")
    print(f"     math.sqrt(16) = {math.sqrt(16)}")
    print(f"     math.ceil(4.2)  = {math.ceil(4.2)}")
    print(f"     math.floor(4.9) = {math.floor(4.9)}")
    print(f"     math.log2(8)    = {math.log2(8)}")
    print(f"     math.gcd(12,8)  = {math.gcd(12, 8)}")

    # --- datetime module ---
    print(f"\n   datetime module:")
    now = datetime.datetime.now()
    print(f"     Current time:  {now}")
    print(f"     Formatted:     {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"     Date only:     {now.date()}")
    print(f"     Time only:     {now.time()}")

    future = now + datetime.timedelta(days=30)
    print(f"     30 days later: {future.date()}")

    # --- json module ---
    print(f"\n   json module:")
    data = {"name": "Alice", "age": 30, "skills": ["Python", "SQL"]}
    json_str = json.dumps(data, indent=2)
    print(f"     Python dict  JSON string:")
    for line in json_str.split("\n"):
        print(f"       {line}")

    parsed = json.loads(json_str)
    print(f"     JSON string  Python dict: {parsed}")

    # --- os module ---
    print(f"\n   os module:")
    print(f"     Current directory: {os.getcwd()}")
    print(f"     OS name:          {os.name}")
    print(f"     CPU count:        {os.cpu_count()}")
    print(f"     Path separator:   {os.sep}")

    # --- sys module ---
    print(f"\n    sys module:")
    print(f"     Python version:   {sys.version}")
    print(f"     Platform:         {sys.platform}")
    print(f"     Max integer size: {sys.maxsize}")
    print(f"     Executable:       {sys.executable}")

    print()


# ============================================================================
# Main Execution
# ============================================================================
if __name__ == "__main__":
    print("\n" + " " * 20)
    print("  DAY 9 -- MODULES DEMO")
    print(" " * 20 + "\n")

    demo_name_variable()
    demo_creating_modules()
    demo_sys_path()
    demo_module_inspection()
    demo_package_structure()
    demo_builtin_modules()

    print("=" * 60)
    print(" All module demos completed successfully!")
    print("=" * 60)
