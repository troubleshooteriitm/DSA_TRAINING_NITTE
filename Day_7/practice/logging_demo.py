"""
Logging Module -- Practice Examples

This module demonstrates the Python `logging` module:
1. Basic logging with different levels
2. Logging to a file
3. Formatted logging with custom formatters
4. Rotating file handler (concept & usage)
5. Using multiple handlers simultaneously
6. Logging exceptions with traceback
7. Logger hierarchy and propagation
8. Best practices

Note:
    Examples 2 and 4 create log files in the current directory.
    Clean up generated .log files after running.
"""

import logging
import os
import sys
from logging.handlers import RotatingFileHandler


# ============================================================
# 1. Basic Logging
# ============================================================

def demo_basic_logging():
    """
    Demonstrates basic logging at all five levels.

    The default level is WARNING, so DEBUG and INFO messages
    won't appear unless you configure the level.
    """
    print("\n" + "=" * 50)
    print("  DEMO 1: Basic Logging")
    print("=" * 50)

    # Configure root logger to show ALL levels
    # WARNING: basicConfig only works if root logger has no handlers yet.
    # We use force=True to reset any existing configuration.
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(levelname)-8s : %(message)s",
        force=True,  # Python 3.8+ -- reset existing config
    )

    # Log at each level
    logging.debug("This is a DEBUG message -- detailed diagnostic info")
    logging.info("This is an INFO message -- things are working fine")
    logging.warning("This is a WARNING message -- something unexpected")
    logging.error("This is an ERROR message -- something went wrong")
    logging.critical("This is a CRITICAL message -- system may crash")

    print("\n  Level hierarchy (lowest to highest):")
    print("  DEBUG(10) < INFO(20) < WARNING(30) < ERROR(40) < CRITICAL(50)")
    print("  Setting level=WARNING means only WARNING, ERROR, CRITICAL appear.")


# ============================================================
# 2. Logging to a File
# ============================================================

def demo_file_logging():
    """
    Demonstrates logging output to a file.

    Creates 'demo_app.log' in the current directory.
    """
    print("\n" + "=" * 50)
    print("  DEMO 2: File Logging")
    print("=" * 50)

    # Create a named logger (not the root logger)
    file_logger = logging.getLogger("file_demo")
    file_logger.setLevel(logging.DEBUG)

    # Remove any existing handlers to avoid duplicate messages
    file_logger.handlers.clear()

    # Create a file handler
    log_filepath = "demo_app.log"
    file_handler = logging.FileHandler(log_filepath, mode="w")
    file_handler.setLevel(logging.DEBUG)

    # Create a simple formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    # Add handler to logger
    file_logger.addHandler(file_handler)

    # Prevent messages from propagating to root logger
    file_logger.propagate = False

    # Log some messages
    file_logger.debug("Debug message -- written to file")
    file_logger.info("Info message -- written to file")
    file_logger.warning("Warning message -- written to file")
    file_logger.error("Error message -- written to file")
    file_logger.critical("Critical message -- written to file")

    # Read and display the log file contents
    file_handler.flush()
    with open(log_filepath, "r") as f:
        contents = f.read()

    print(f"\n  Log file '{log_filepath}' contents:\n")
    for line in contents.strip().split("\n"):
        print(f"    {line}")

    # Clean up the handler
    file_logger.removeHandler(file_handler)
    file_handler.close()

    # Clean up log file
    if os.path.exists(log_filepath):
        os.remove(log_filepath)
        print(f"\n  (Cleaned up '{log_filepath}')")


# ============================================================
# 3. Formatted Logging
# ============================================================

def demo_formatted_logging():
    """
    Demonstrates custom log formatting with various attributes.
    """
    print("\n" + "=" * 50)
    print("  DEMO 3: Formatted Logging")
    print("=" * 50)

    # Create a named logger
    fmt_logger = logging.getLogger("format_demo")
    fmt_logger.setLevel(logging.DEBUG)
    fmt_logger.handlers.clear()
    fmt_logger.propagate = False

    # --- Format 1: Simple format ---
    print("\n  Format 1 -- Simple:")
    simple_handler = logging.StreamHandler(sys.stdout)
    simple_formatter = logging.Formatter("%(levelname)s: %(message)s")
    simple_handler.setFormatter(simple_formatter)
    fmt_logger.addHandler(simple_handler)

    fmt_logger.info("Simple format example")
    fmt_logger.removeHandler(simple_handler)

    # --- Format 2: Detailed format ---
    print("\n  Format 2 -- Detailed:")
    detailed_handler = logging.StreamHandler(sys.stdout)
    detailed_formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)-8s | "
        "%(filename)s:%(lineno)d | %(message)s",
        datefmt="%H:%M:%S",
    )
    detailed_handler.setFormatter(detailed_formatter)
    fmt_logger.addHandler(detailed_handler)

    fmt_logger.warning("Detailed format example")
    fmt_logger.removeHandler(detailed_handler)

    # --- Format 3: JSON-like format ---
    print("\n  Format 3 -- JSON-like:")
    json_handler = logging.StreamHandler(sys.stdout)
    json_formatter = logging.Formatter(
        '{"time": "%(asctime)s", "level": "%(levelname)s", '
        '"module": "%(module)s", "func": "%(funcName)s", '
        '"message": "%(message)s"}',
        datefmt="%Y-%m-%dT%H:%M:%S",
    )
    json_handler.setFormatter(json_formatter)
    fmt_logger.addHandler(json_handler)

    fmt_logger.error("JSON-like format example")
    fmt_logger.removeHandler(json_handler)

    # Show all available format attributes
    print("\n  Common format attributes:")
    attributes = [
        ("%(asctime)s", "Human-readable timestamp"),
        ("%(levelname)s", "Log level name (DEBUG, INFO, etc.)"),
        ("%(name)s", "Logger name"),
        ("%(message)s", "The log message"),
        ("%(filename)s", "Source filename"),
        ("%(lineno)d", "Line number in source"),
        ("%(funcName)s", "Function name"),
        ("%(module)s", "Module name (filename without extension)"),
        ("%(pathname)s", "Full path of source file"),
        ("%(process)d", "Process ID"),
        ("%(thread)d", "Thread ID"),
    ]
    for attr, desc in attributes:
        print(f"    {attr:<20s} -- {desc}")


# ============================================================
# 4. Rotating File Handler
# ============================================================

def demo_rotating_handler():
    """
    Demonstrates RotatingFileHandler to prevent log files from
    growing indefinitely.

    The handler automatically rotates the log file when it reaches
    a specified size, keeping a configurable number of backup files.
    """
    print("\n" + "=" * 50)
    print("  DEMO 4: Rotating File Handler")
    print("=" * 50)

    # Create a named logger
    rot_logger = logging.getLogger("rotating_demo")
    rot_logger.setLevel(logging.DEBUG)
    rot_logger.handlers.clear()
    rot_logger.propagate = False

    # Create a rotating file handler
    # maxBytes: max size per log file before rotation
    # backupCount: number of backup files to keep
    log_file = "rotating_demo.log"
    rotating_handler = RotatingFileHandler(
        log_file,
        maxBytes=500,      # Rotate after 500 bytes (tiny, for demo)
        backupCount=3,     # Keep up to 3 backup files
    )
    rotating_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%H:%M:%S",
    )
    rotating_handler.setFormatter(formatter)
    rot_logger.addHandler(rotating_handler)

    # Write many messages to trigger rotation
    for i in range(1, 21):
        rot_logger.info(
            "Log entry #%02d -- This message contributes to file rotation", i
        )

    # Flush and close
    rotating_handler.flush()
    rot_logger.removeHandler(rotating_handler)
    rotating_handler.close()

    # Show which files were created
    print("\n  Generated log files:")
    log_files = [
        f for f in os.listdir(".")
        if f.startswith("rotating_demo.log")
    ]
    for lf in sorted(log_files):
        size = os.path.getsize(lf)
        print(f"    {lf:<30s} -- {size:>5d} bytes")

    # Show contents of the main (most recent) log file
    with open(log_file, "r") as f:
        lines = f.readlines()
    print(f"\n  Last entries in '{log_file}':")
    for line in lines[-3:]:
        print(f"    {line.strip()}")

    # Clean up all generated log files
    for lf in log_files:
        os.remove(lf)
    print(f"\n  (Cleaned up {len(log_files)} log file(s))")


# ============================================================
# 5. Multiple Handlers (Console + File)
# ============================================================

def demo_multiple_handlers():
    """
    Demonstrates using multiple handlers on a single logger:
    - Console handler: shows WARNING and above
    - File handler: records DEBUG and above

    This is a common production pattern where you want detailed
    logs in files but only important messages on the console.
    """
    print("\n" + "=" * 50)
    print("  DEMO 5: Multiple Handlers")
    print("=" * 50)

    # Create a named logger
    multi_logger = logging.getLogger("multi_demo")
    multi_logger.setLevel(logging.DEBUG)
    multi_logger.handlers.clear()
    multi_logger.propagate = False

    # Console handler -- WARNING and above only
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.WARNING)
    console_fmt = logging.Formatter(
        "  [CONSOLE] %(levelname)-8s: %(message)s"
    )
    console_handler.setFormatter(console_fmt)

    # File handler -- everything (DEBUG and above)
    log_file = "multi_demo.log"
    file_handler = logging.FileHandler(log_file, mode="w")
    file_handler.setLevel(logging.DEBUG)
    file_fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%H:%M:%S",
    )
    file_handler.setFormatter(file_fmt)

    # Attach both handlers
    multi_logger.addHandler(console_handler)
    multi_logger.addHandler(file_handler)

    # Log messages at various levels
    print("\n  Messages sent (console shows WARNING+ only):\n")
    multi_logger.debug("Debug: detailed trace info")
    multi_logger.info("Info: operation completed")
    multi_logger.warning("Warning: disk space low")
    multi_logger.error("Error: connection refused")
    multi_logger.critical("Critical: system overheating")

    # Show file contents (has all messages)
    file_handler.flush()
    with open(log_file, "r") as f:
        contents = f.read()

    print(f"\n  File '{log_file}' contents (has ALL levels):\n")
    for line in contents.strip().split("\n"):
        print(f"    {line}")

    # Clean up
    multi_logger.removeHandler(console_handler)
    multi_logger.removeHandler(file_handler)
    file_handler.close()
    if os.path.exists(log_file):
        os.remove(log_file)
        print(f"\n  (Cleaned up '{log_file}')")


# ============================================================
# 6. Logging Exceptions with Traceback
# ============================================================

def demo_exception_logging():
    """
    Demonstrates logging exceptions with full traceback
    using logger.exception() or logger.error(..., exc_info=True).
    """
    print("\n" + "=" * 50)
    print("  DEMO 6: Logging Exceptions")
    print("=" * 50)

    # Create a named logger
    exc_logger = logging.getLogger("exception_demo")
    exc_logger.setLevel(logging.DEBUG)
    exc_logger.handlers.clear()
    exc_logger.propagate = False

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        "  %(levelname)s: %(message)s"
    ))
    exc_logger.addHandler(handler)

    # Method 1: logger.exception() -- always logs at ERROR level
    print("\n  Method 1 -- logger.exception():\n")
    try:
        result = 10 / 0
    except ZeroDivisionError:
        exc_logger.exception("Division failed")

    # Method 2: logger.error() with exc_info=True
    print("\n  Method 2 -- logger.error(exc_info=True):\n")
    try:
        data = {"key": "value"}
        _ = data["missing_key"]
    except KeyError:
        exc_logger.error("Key lookup failed", exc_info=True)

    # Method 3: Using exc_info with any level
    print("\n  Method 3 -- logger.warning(exc_info=True):\n")
    try:
        int("not_a_number")
    except ValueError:
        exc_logger.warning("Non-critical parse failure", exc_info=True)

    exc_logger.removeHandler(handler)


# ============================================================
# 7. Logger Hierarchy and Propagation
# ============================================================

def demo_logger_hierarchy():
    """
    Demonstrates how loggers form a hierarchy based on dot-separated
    names, and how propagation works.

    Logger 'myapp.database.queries' is a child of 'myapp.database',
    which is a child of 'myapp'.
    """
    print("\n" + "=" * 50)
    print("  DEMO 7: Logger Hierarchy & Propagation")
    print("=" * 50)

    # Create parent logger
    parent = logging.getLogger("myapp")
    parent.setLevel(logging.DEBUG)
    parent.handlers.clear()

    parent_handler = logging.StreamHandler(sys.stdout)
    parent_handler.setFormatter(logging.Formatter(
        "  [myapp handler]     %(name)-25s | %(message)s"
    ))
    parent.addHandler(parent_handler)

    # Create child logger
    child = logging.getLogger("myapp.database")
    child.handlers.clear()

    child_handler = logging.StreamHandler(sys.stdout)
    child_handler.setFormatter(logging.Formatter(
        "  [db handler]        %(name)-25s | %(message)s"
    ))
    child.addHandler(child_handler)

    # Create grandchild logger (no handler of its own)
    grandchild = logging.getLogger("myapp.database.queries")

    print("\n  With propagation enabled (default):")
    print("  (Messages bubble up to parent handlers)\n")

    # This will print TWICE -- once from child handler, once from parent
    child.info("Database connection established")

    # This will print TWICE -- propagates up through the chain
    grandchild.warning("Slow query detected")

    print("\n  With propagation disabled on 'myapp.database':")
    child.propagate = False
    child.info("This only appears in db handler")
    grandchild.info("This also only appears in db handler (via parent)")

    # Reset propagation
    child.propagate = True

    # Clean up
    parent.removeHandler(parent_handler)
    child.removeHandler(child_handler)


# ============================================================
# 8. Best Practices Summary
# ============================================================

def demo_best_practices():
    """
    Summarizes logging best practices.
    """
    print("\n" + "=" * 50)
    print("  DEMO 8: Logging Best Practices")
    print("=" * 50)

    practices = [
        (
            "Use __name__ for logger names",
            "logger = logging.getLogger(__name__)",
            "Creates a hierarchy matching your package structure.",
        ),
        (
            "Don't use print() for logging",
            "logger.info('message') instead of print('message')",
            "Logging is configurable, filterable, and redirectable.",
        ),
        (
            "Use appropriate log levels",
            "DEBUG for dev, INFO for operations, WARNING+ for issues",
            "Makes filtering and alerting possible.",
        ),
        (
            "Use logger.exception() in except blocks",
            "except SomeError: logger.exception('Failed')",
            "Automatically includes the full traceback.",
        ),
        (
            "Configure logging once at the entry point",
            "Set up handlers in main() or a config file",
            "Avoid calling basicConfig() in library code.",
        ),
        (
            "Use lazy string formatting",
            "logger.debug('Value: %s', value)  # NOT f'Value: {value}'",
            "The format string is only evaluated if the level is enabled.",
        ),
        (
            "Use RotatingFileHandler in production",
            "Prevents log files from consuming all disk space",
            "Set maxBytes and backupCount appropriately.",
        ),
    ]

    for i, (title, example, explanation) in enumerate(practices, 1):
        print(f"\n  {i}. {title}")
        print(f"     Example: {example}")
        print(f"     Why: {explanation}")


# ============================================================
# Main -- Run All Demos
# ============================================================

def main():
    """Run all logging demonstrations in sequence."""
    print("\n" + "" * 25)
    print("  PYTHON LOGGING MODULE -- COMPLETE DEMO")
    print("" * 25)

    demo_basic_logging()
    demo_file_logging()
    demo_formatted_logging()
    demo_rotating_handler()
    demo_multiple_handlers()
    demo_exception_logging()
    demo_logger_hierarchy()
    demo_best_practices()

    print("\n" + "=" * 50)
    print("  ALL LOGGING DEMOS COMPLETE")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    main()
