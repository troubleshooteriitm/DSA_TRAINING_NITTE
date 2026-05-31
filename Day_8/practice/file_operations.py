"""
File Operations -- Practice Examples
=====================================
Day 8: File Handling & Data Processing

This script demonstrates:
1. Reading text files (read, readline, readlines)
2. Writing text files (write, writelines)
3. Append mode
4. Binary file operations
5. pathlib usage for modern file handling
6. Context managers (with statement)
7. File metadata and directory operations

All file operations create temporary files in the same directory
as this script, so they are self-contained and runnable.
"""

import os
from pathlib import Path

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent

# Subdirectory for generated practice files
OUTPUT_DIR = SCRIPT_DIR / "generated_files"


# ============================================================
# SETUP -- Create output directory
# ============================================================

def setup():
    """Create the output directory for practice files."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    print(f"   Output directory: {OUTPUT_DIR}\n")


# ============================================================
# 1. WRITING TEXT FILES
# ============================================================

def example_write_text():
    """
    Demonstrate writing text to a file using different methods.
    """
    print("=" * 60)
    print("  Example 1: Writing Text Files")
    print("=" * 60)

    # --- Method 1: write() -- writes a single string ---
    filepath = OUTPUT_DIR / "write_example.txt"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("Hello, World!\n")
        f.write("This is the second line.\n")
        f.write("Python file handling is powerful.\n")

    print(f"   Created: {filepath.name}")

    # --- Method 2: writelines() -- writes a list of strings ---
    filepath2 = OUTPUT_DIR / "writelines_example.txt"
    lines = [
        "Line 1: Introduction\n",
        "Line 2: Body paragraph\n",
        "Line 3: Conclusion\n",
        "Line 4: References\n",
    ]
    with open(filepath2, "w", encoding="utf-8") as f:
        f.writelines(lines)  # Note: writelines does NOT add \n automatically

    print(f"   Created: {filepath2.name}")

    # --- Method 3: print() with file parameter ---
    filepath3 = OUTPUT_DIR / "print_to_file.txt"
    with open(filepath3, "w", encoding="utf-8") as f:
        print("This was written using print()", file=f)
        print(f"Current directory: {os.getcwd()}", file=f)
        print(f"Script location: {SCRIPT_DIR}", file=f)

    print(f"   Created: {filepath3.name}")
    print()


# ============================================================
# 2. READING TEXT FILES
# ============================================================

def example_read_text():
    """
    Demonstrate different methods to read text files.
    """
    print("=" * 60)
    print("  Example 2: Reading Text Files")
    print("=" * 60)

    filepath = OUTPUT_DIR / "write_example.txt"

    # --- Method 1: read() -- read entire file as a single string ---
    print("\n  [read() -- entire file]")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    print(f"  Content ({len(content)} chars):")
    print(f"  {repr(content)}")

    # --- Method 2: readline() -- read one line at a time ---
    print("\n  [readline() -- one line at a time]")
    with open(filepath, "r", encoding="utf-8") as f:
        line1 = f.readline()
        line2 = f.readline()
    print(f"  Line 1: {line1.strip()}")
    print(f"  Line 2: {line2.strip()}")

    # --- Method 3: readlines() -- read all lines as a list ---
    print("\n  [readlines() -- all lines as list]")
    with open(filepath, "r", encoding="utf-8") as f:
        all_lines = f.readlines()
    print(f"  Total lines: {len(all_lines)}")
    for i, line in enumerate(all_lines):
        print(f"    [{i}]: {line.strip()}")

    # --- Method 4: Iterate line by line (memory efficient) ---
    print("\n  [for loop -- memory efficient iteration]")
    with open(filepath, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            print(f"    Line {line_num}: {line.strip()}")

    print()


# ============================================================
# 3. APPEND MODE
# ============================================================

def example_append_mode():
    """
    Demonstrate appending to files without overwriting existing content.
    """
    print("=" * 60)
    print("  Example 3: Append Mode")
    print("=" * 60)

    filepath = OUTPUT_DIR / "append_example.txt"

    # First, create the file with initial content
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("=== Log Started ===\n")
        f.write("Entry 1: System initialized\n")

    print("   Initial file created")

    # Now APPEND additional entries (original content is preserved)
    with open(filepath, "a", encoding="utf-8") as f:
        f.write("Entry 2: User logged in\n")
        f.write("Entry 3: Data processed\n")

    print("   Appended 2 entries")

    # Append more entries
    with open(filepath, "a", encoding="utf-8") as f:
        f.write("Entry 4: Report generated\n")
        f.write("=== Log Ended ===\n")

    print("   Appended 2 more entries")

    # Read and display the complete file
    print("\n  Complete file contents:")
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            print(f"    {line.strip()}")

    print()


# ============================================================
# 4. BINARY FILE OPERATIONS
# ============================================================

def example_binary_files():
    """
    Demonstrate reading and writing binary files.
    Binary mode is essential for non-text files (images, PDFs, etc.).
    """
    print("=" * 60)
    print("  Example 4: Binary File Operations")
    print("=" * 60)

    filepath = OUTPUT_DIR / "binary_example.bin"

    # --- Writing binary data ---
    # Create some sample binary data
    binary_data = bytes(range(256))  # All possible byte values (0-255)

    with open(filepath, "wb") as f:
        f.write(binary_data)

    print(f"   Written {len(binary_data)} bytes to: {filepath.name}")

    # --- Reading binary data ---
    with open(filepath, "rb") as f:
        read_data = f.read()

    print(f"   Read {len(read_data)} bytes from: {filepath.name}")
    print(f"  First 16 bytes (hex): {read_data[:16].hex(' ')}")
    print(f"  Last 16 bytes (hex):  {read_data[-16:].hex(' ')}")

    # Verify data integrity
    assert binary_data == read_data, "Binary data mismatch!"
    print("   Data integrity verified (write == read)")

    # --- Copying a binary file ---
    copy_path = OUTPUT_DIR / "binary_copy.bin"
    with open(filepath, "rb") as src, open(copy_path, "wb") as dst:
        dst.write(src.read())

    print(f"   Copied to: {copy_path.name}")

    # --- Reading binary in chunks (memory efficient for large files) ---
    print("\n  [Reading in 64-byte chunks]")
    chunk_count = 0
    with open(filepath, "rb") as f:
        while True:
            chunk = f.read(64)  # Read 64 bytes at a time
            if not chunk:
                break
            chunk_count += 1

    print(f"  Read file in {chunk_count} chunks of 64 bytes each")
    print()


# ============================================================
# 5. PATHLIB USAGE
# ============================================================

def example_pathlib():
    """
    Demonstrate modern file handling using pathlib.Path.
    pathlib is the recommended approach for new Python code.
    """
    print("=" * 60)
    print("  Example 5: pathlib -- Modern File Handling")
    print("=" * 60)

    # --- Creating paths ---
    print("\n  [Path Construction]")
    base = Path("D:/projects")
    project = base / "my_app" / "src" / "main.py"
    print(f"  Constructed path: {project}")

    # --- Path properties ---
    print("\n  [Path Properties]")
    sample_path = Path("/home/user/documents/report_2025.pdf")
    print(f"  Full path:  {sample_path}")
    print(f"  Name:       {sample_path.name}")       # report_2025.pdf
    print(f"  Stem:       {sample_path.stem}")       # report_2025
    print(f"  Suffix:     {sample_path.suffix}")     # .pdf
    print(f"  Parent:     {sample_path.parent}")     # /home/user/documents
    print(f"  Parts:      {sample_path.parts}")      # Tuple of path components

    # --- Convenience methods: read_text / write_text ---
    print("\n  [Convenience: read_text / write_text]")
    text_path = OUTPUT_DIR / "pathlib_example.txt"
    text_path.write_text(
        "Written with pathlib!\nNo need for open() or close().\n",
        encoding="utf-8"
    )
    content = text_path.read_text(encoding="utf-8")
    print(f"  Written and read back: {content.strip()}")

    # --- Convenience methods: read_bytes / write_bytes ---
    print("\n  [Convenience: read_bytes / write_bytes]")
    bin_path = OUTPUT_DIR / "pathlib_binary.bin"
    bin_path.write_bytes(b"Hello in bytes! \x00\x01\x02")
    data = bin_path.read_bytes()
    print(f"  Binary data ({len(data)} bytes): {data}")

    # --- Checking existence ---
    print("\n  [Existence Checks]")
    print(f"  {text_path.name} exists? {text_path.exists()}")
    print(f"  {text_path.name} is file? {text_path.is_file()}")
    print(f"  {OUTPUT_DIR.name} is dir?  {OUTPUT_DIR.is_dir()}")
    fake_path = Path("this/does/not/exist.txt")
    print(f"  Non-existent path exists? {fake_path.exists()}")

    # --- Creating directories ---
    print("\n  [Creating Directories]")
    nested_dir = OUTPUT_DIR / "level1" / "level2" / "level3"
    nested_dir.mkdir(parents=True, exist_ok=True)
    print(f"  Created nested directory: {nested_dir}")

    # --- Globbing (finding files by pattern) ---
    print("\n  [Globbing -- Find files by pattern]")
    print(f"  .txt files in output dir:")
    for txt_file in OUTPUT_DIR.glob("*.txt"):
        size = txt_file.stat().st_size
        print(f"    {txt_file.name} ({size} bytes)")

    print(f"\n  All .py files in script directory (recursive):")
    for py_file in SCRIPT_DIR.glob("**/*.py"):
        print(f"    {py_file.relative_to(SCRIPT_DIR)}")

    # --- Iterating directory contents ---
    print(f"\n  [Directory Contents: {OUTPUT_DIR.name}/]")
    for item in sorted(OUTPUT_DIR.iterdir()):
        if item.is_file():
            size = item.stat().st_size
            print(f"     {item.name:<30} ({size:>6} bytes)")
        elif item.is_dir():
            print(f"     {item.name}/")

    print()


# ============================================================
# 6. FILE METADATA WITH os.path
# ============================================================

def example_file_metadata():
    """
    Demonstrate retrieving file metadata using os.path and pathlib.
    """
    print("=" * 60)
    print("  Example 6: File Metadata")
    print("=" * 60)

    # Use an existing file for metadata
    filepath = OUTPUT_DIR / "write_example.txt"

    if not filepath.exists():
        print("    Example file not found. Run example 1 first.")
        return

    # --- os.path methods ---
    print("\n  [os.path metadata]")
    str_path = str(filepath)
    print(f"  Basename:     {os.path.basename(str_path)}")
    print(f"  Dirname:      {os.path.dirname(str_path)}")
    print(f"  Extension:    {os.path.splitext(str_path)[1]}")
    print(f"  Absolute:     {os.path.abspath(str_path)}")
    print(f"  File size:    {os.path.getsize(str_path)} bytes")
    print(f"  Is file:      {os.path.isfile(str_path)}")
    print(f"  Is dir:       {os.path.isdir(str_path)}")

    # --- pathlib stat() for detailed metadata ---
    print("\n  [pathlib stat() metadata]")
    stat = filepath.stat()
    from datetime import datetime
    created = datetime.fromtimestamp(stat.st_ctime)
    modified = datetime.fromtimestamp(stat.st_mtime)
    print(f"  File:         {filepath.name}")
    print(f"  Size:         {stat.st_size} bytes")
    print(f"  Created:      {created.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Modified:     {modified.strftime('%Y-%m-%d %H:%M:%S')}")

    print()


# ============================================================
# 7. PRACTICAL EXAMPLE -- LINE COUNTER
# ============================================================

def example_line_counter():
    """
    Practical example: Count lines, words, and characters in files.
    Mimics the Unix 'wc' command.
    """
    print("=" * 60)
    print("  Example 7: Line/Word/Character Counter (like wc)")
    print("=" * 60)

    # Create a sample file to analyze
    sample_path = OUTPUT_DIR / "sample_text.txt"
    sample_text = (
        "Python is a versatile programming language.\n"
        "It supports multiple programming paradigms.\n"
        "File handling is essential for data processing.\n"
        "The pathlib module provides an object-oriented interface.\n"
        "Context managers ensure proper resource cleanup.\n"
    )
    sample_path.write_text(sample_text, encoding="utf-8")

    # Count lines, words, and characters
    with open(sample_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    total_lines = len(lines)
    total_words = sum(len(line.split()) for line in lines)
    total_chars = sum(len(line) for line in lines)

    print(f"\n  File: {sample_path.name}")
    print(f"  ")
    print(f"  Lines:      {total_lines:>6}")
    print(f"  Words:      {total_words:>6}")
    print(f"  Characters: {total_chars:>6}")

    # Count per line
    print(f"\n  Per-line breakdown:")
    for i, line in enumerate(lines, start=1):
        words = len(line.split())
        chars = len(line.strip())
        print(f"    Line {i}: {words:>3} words, {chars:>3} chars | {line.strip()}")

    print()


# ============================================================
# 8. ERROR HANDLING IN FILE OPERATIONS
# ============================================================

def example_error_handling():
    """
    Demonstrate proper error handling for file operations.
    """
    print("=" * 60)
    print("  Example 8: Error Handling in File I/O")
    print("=" * 60)

    # --- FileNotFoundError ---
    print("\n  [FileNotFoundError]")
    try:
        with open("nonexistent_file_xyz.txt", "r") as f:
            content = f.read()
    except FileNotFoundError as e:
        print(f"   Caught: {type(e).__name__}: {e}")

    # --- PermissionError (simulated) ---
    print("\n  [PermissionError -- checking before writing]")
    test_path = OUTPUT_DIR / "permission_test.txt"
    if test_path.parent.exists():
        print(f"   Directory writable: {test_path.parent}")
    else:
        print(f"    Directory does not exist: {test_path.parent}")

    # --- IsADirectoryError ---
    print("\n  [IsADirectoryError]")
    try:
        with open(str(OUTPUT_DIR), "r") as f:
            content = f.read()
    except (IsADirectoryError, PermissionError) as e:
        print(f"   Caught: {type(e).__name__}: {e}")

    # --- General error handling pattern ---
    print("\n  [General safe file reading pattern]")
    safe_path = OUTPUT_DIR / "write_example.txt"
    try:
        with open(safe_path, "r", encoding="utf-8") as f:
            content = f.read()
        print(f"   Successfully read {len(content)} characters")
    except FileNotFoundError:
        print(f"   File not found: {safe_path}")
    except PermissionError:
        print(f"   Permission denied: {safe_path}")
    except UnicodeDecodeError:
        print(f"   File encoding error: {safe_path}")
    except OSError as e:
        print(f"   OS error: {e}")

    print()


# ============================================================
# CLEANUP
# ============================================================

def cleanup(keep_files: bool = True):
    """
    Optionally clean up generated practice files.

    Args:
        keep_files: If True, files are kept for inspection.
    """
    if keep_files:
        print("   Generated files kept in: generated_files/")
        print("     Delete manually when no longer needed.")
    else:
        import shutil
        if OUTPUT_DIR.exists():
            shutil.rmtree(OUTPUT_DIR)
            print("   Cleaned up all generated files.")


# ============================================================
# MAIN EXECUTION
# ============================================================

def main():
    """Run all file operations examples."""
    print("\n" + "" * 60)
    print("  File Operations -- Practice Examples")
    print("" * 60 + "\n")

    # Setup
    setup()

    # Run all examples
    example_write_text()
    example_read_text()
    example_append_mode()
    example_binary_files()
    example_pathlib()
    example_file_metadata()
    example_line_counter()
    example_error_handling()

    # Keep generated files for inspection
    print("=" * 60)
    cleanup(keep_files=True)

    print("\n" + "" * 60)
    print("  All file operations examples completed successfully! ")
    print("" * 60 + "\n")


if __name__ == "__main__":
    main()
