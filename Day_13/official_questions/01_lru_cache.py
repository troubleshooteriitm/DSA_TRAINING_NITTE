"""
LeetCode 146 -- LRU Cache
=========================
Difficulty: Medium
URL: https://leetcode.com/problems/lru-cache/

Problem Description:
    Design a data structure that follows the constraints of a
    Least Recently Used (LRU) cache.

    Implement the LRUCache class:
    - LRUCache(int capacity): Initialize the LRU cache with positive size capacity.
    - int get(int key): Return the value of the key if the key exists,
      otherwise return -1.
    - void put(int key, int value): Update the value of the key if the key exists.
      Otherwise, add the key-value pair to the cache. If the number of keys exceeds
      the capacity from this operation, evict the least recently used key.

    Both get() and put() must run in O(1) average time complexity.

Approach:
    We use Python's OrderedDict which maintains insertion order and supports
    O(1) move_to_end() and popitem() operations.

    - get(key): If key exists, move it to the end (most recently used) and return value.
    - put(key, value): If key exists, update and move to end. If not, insert it.
      If capacity is exceeded, remove the first item (least recently used).

    Alternative: Use a dict (Python 3.7+ guarantees insertion order) with manual
    re-insertion for "move to end" behavior.

Time Complexity: O(1) for both get() and put()
Space Complexity: O(capacity)
"""

from collections import OrderedDict


class LRUCache:
    """
    Least Recently Used (LRU) Cache implementation using OrderedDict.

    The OrderedDict maintains keys in insertion order. When a key is accessed
    or updated, it is moved to the end (most recently used position).
    When capacity is exceeded, the first item (least recently used) is removed.
    """

    def __init__(self, capacity: int):
        """
        Initialize the LRU Cache.

        Args:
            capacity: Maximum number of key-value pairs the cache can hold.
        """
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        """
        Retrieve value for the given key.

        If the key exists, mark it as most recently used by moving
        it to the end of the OrderedDict.

        Args:
            key: The key to look up.

        Returns:
            The value if key exists, -1 otherwise.
        """
        if key not in self.cache:
            return -1

        # Move to end to mark as most recently used
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        """
        Insert or update a key-value pair.

        If the key already exists, update its value and move to end.
        If inserting a new key would exceed capacity, evict the least
        recently used item (first item in OrderedDict).

        Args:
            key: The key to insert or update.
            value: The value to associate with the key.
        """
        if key in self.cache:
            # Update existing key and move to end (most recently used)
            self.cache.move_to_end(key)
            self.cache[key] = value
        else:
            # Check if we need to evict before inserting
            if len(self.cache) >= self.capacity:
                # popitem(last=False) removes the first item (LRU)
                self.cache.popitem(last=False)
            self.cache[key] = value


class LRUCacheDictBased:
    """
    Alternative LRU Cache implementation using plain dict (Python 3.7+).

    Python 3.7+ guarantees dict maintains insertion order. We simulate
    move_to_end by deleting and re-inserting the key.
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        # Move to end by re-inserting
        value = self.cache.pop(key)
        self.cache[key] = value
        return value

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # Remove and re-insert to move to end
            del self.cache[key]
        elif len(self.cache) >= self.capacity:
            # Remove the first (oldest/LRU) key
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
        self.cache[key] = value


# ============================================================
# Test Cases
# ============================================================

if __name__ == '__main__':

    # --- Test LRUCache (OrderedDict-based) ---

    # Test 1: Basic operations from LeetCode example
    cache = LRUCache(2)
    cache.put(1, 1)                          # cache: {1=1}
    cache.put(2, 2)                          # cache: {1=1, 2=2}
    assert cache.get(1) == 1                 # returns 1, cache: {2=2, 1=1}
    cache.put(3, 3)                          # evicts key 2, cache: {1=1, 3=3}
    assert cache.get(2) == -1                # returns -1 (not found)
    cache.put(4, 4)                          # evicts key 1, cache: {3=3, 4=4}
    assert cache.get(1) == -1                # returns -1 (evicted)
    assert cache.get(3) == 3                 # returns 3
    assert cache.get(4) == 4                 # returns 4

    # Test 2: Update existing key
    cache2 = LRUCache(2)
    cache2.put(1, 10)
    cache2.put(2, 20)
    cache2.put(1, 100)                       # Update key 1
    assert cache2.get(1) == 100              # Updated value
    cache2.put(3, 30)                        # Should evict key 2 (LRU)
    assert cache2.get(2) == -1               # Key 2 was evicted
    assert cache2.get(3) == 30

    # Test 3: Single capacity
    cache3 = LRUCache(1)
    cache3.put(1, 1)
    assert cache3.get(1) == 1
    cache3.put(2, 2)                         # Evicts key 1
    assert cache3.get(1) == -1
    assert cache3.get(2) == 2

    # Test 4: Get non-existent key
    cache4 = LRUCache(3)
    assert cache4.get(99) == -1

    # --- Test LRUCacheDictBased ---

    # Repeat Test 1 with dict-based implementation
    cache_dict = LRUCacheDictBased(2)
    cache_dict.put(1, 1)
    cache_dict.put(2, 2)
    assert cache_dict.get(1) == 1
    cache_dict.put(3, 3)
    assert cache_dict.get(2) == -1
    cache_dict.put(4, 4)
    assert cache_dict.get(1) == -1
    assert cache_dict.get(3) == 3
    assert cache_dict.get(4) == 4

    print("All test cases passed!")
