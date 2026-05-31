"""
Decorators Demo
================
Practical decorator examples: timer, logging, retry, and auth check.
"""

import time
import functools


# ============================================================
# 1. TIMER DECORATOR
# ============================================================

def timer(func):
    """Measure execution time of a function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"  {func.__name__}() executed in {elapsed:.4f} seconds")
        return result
    return wrapper


@timer
def slow_function():
    """Simulate a slow operation."""
    total = sum(i * i for i in range(1_000_000))
    return total


# ============================================================
# 2. LOGGING DECORATOR
# ============================================================

def log_calls(func):
    """Log function calls with arguments and return values."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_str = ", ".join(
            [repr(a) for a in args] +
            [f"{k}={v!r}" for k, v in kwargs.items()]
        )
        print(f" CALL: {func.__name__}({args_str})")
        result = func(*args, **kwargs)
        print(f" RETURN: {func.__name__}  {result!r}")
        return result
    return wrapper


@log_calls
def add(a, b):
    return a + b


@log_calls
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"


# ============================================================
# 3. RETRY DECORATOR
# ============================================================

def retry(max_attempts=3, delay=0.1):
    """Retry a function on failure with configurable attempts and delay."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f" Attempt {attempt}/{max_attempts} failed: {e}")
                    if attempt < max_attempts:
                        time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator


call_count = 0

@retry(max_attempts=3, delay=0.05)
def unreliable_function():
    """Simulates a function that fails the first 2 times."""
    global call_count
    call_count += 1
    if call_count < 3:
        raise ConnectionError(f"Simulated failure #{call_count}")
    return "Success on attempt 3!"


# ============================================================
# 4. AUTH CHECK DECORATOR
# ============================================================

def require_role(*allowed_roles):
    """Check if the current user has the required role."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(user, *args, **kwargs):
            user_role = user.get("role", "guest")
            if user_role not in allowed_roles:
                print(f" ACCESS DENIED: {user.get('name', 'Unknown')} "
                      f"(role: {user_role}) cannot access {func.__name__}()")
                return None
            print(f" ACCESS GRANTED: {user.get('name', 'Unknown')} "
                  f"(role: {user_role})")
            return func(user, *args, **kwargs)
        return wrapper
    return decorator


@require_role("admin", "manager")
def delete_record(user, record_id):
    return f"Record {record_id} deleted by {user['name']}"


@require_role("admin")
def reset_system(user):
    return f"System reset initiated by {user['name']}"


# ============================================================
# 5. CHAINING DECORATORS
# ============================================================

@timer
@log_calls
def compute_factorial(n):
    """Demonstrates chaining decorators."""
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":
    print("=" * 50)
    print("  DECORATORS DEMO")
    print("=" * 50)

    # Timer
    print("\n--- Timer Decorator ---")
    slow_function()

    # Logging
    print("\n--- Logging Decorator ---")
    add(3, 5)
    greet("Alice", greeting="Hi")

    # Retry
    print("\n--- Retry Decorator ---")
    call_count = 0
    result = unreliable_function()
    print(f"Final result: {result}")

    # Auth
    print("\n--- Auth Check Decorator ---")
    admin = {"name": "Alice", "role": "admin"}
    dev = {"name": "Bob", "role": "developer"}

    delete_record(admin, "REC-001")
    delete_record(dev, "REC-002")
    reset_system(admin)
    reset_system(dev)

    # Chaining
    print("\n--- Chained Decorators ---")
    compute_factorial(10)
