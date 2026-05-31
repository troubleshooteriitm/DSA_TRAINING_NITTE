"""
LeetCode 121 - Best Time to Buy and Sell Stock

Problem:
    You are given an array prices where prices[i] is the price of a given
    stock on the ith day.

    You want to maximize your profit by choosing a single day to buy one
    stock and choosing a different day in the future to sell that stock.

    Return the maximum profit you can achieve from this transaction.
    If you cannot achieve any profit, return 0.

Example 1:
    Input: prices = [7, 1, 5, 3, 6, 4]
    Output: 5
    Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6),
                 profit = 6 - 1 = 5.

Example 2:
    Input: prices = [7, 6, 4, 3, 1]
    Output: 0
    Explanation: No profitable transaction is possible.

Approach: Single Pass
    - Track the minimum price seen so far.
    - At each step, calculate the profit if we sell today.
    - Update the maximum profit if current profit is higher.
    - Time Complexity: O(n)
    - Space Complexity: O(1)
"""

from typing import List


def max_profit(prices: List[int]) -> int:
    """
    Find the maximum profit from a single buy-sell transaction.

    Args:
        prices: List of stock prices by day.

    Returns:
        Maximum profit achievable. Returns 0 if no profit is possible.
    """
    if not prices or len(prices) < 2:
        return 0

    min_price = prices[0]   # Track the lowest price seen so far
    best_profit = 0         # Track the best profit achievable

    for price in prices[1:]:
        # Calculate profit if we sell at today's price
        profit = price - min_price

        # Update best profit if this is better
        best_profit = max(best_profit, profit)

        # Update minimum price if today's price is lower
        min_price = min(min_price, price)

    return best_profit


def max_profit_with_days(prices: List[int]) -> tuple:
    """
    Variant that also returns the buy and sell day indices.

    Args:
        prices: List of stock prices by day.

    Returns:
        Tuple of (max_profit, buy_day, sell_day).
        Returns (0, -1, -1) if no profitable transaction exists.
    """
    if not prices or len(prices) < 2:
        return 0, -1, -1

    min_price = prices[0]
    best_profit = 0
    buy_day = 0
    sell_day = -1
    temp_buy = 0

    for i in range(1, len(prices)):
        profit = prices[i] - min_price

        if profit > best_profit:
            best_profit = profit
            buy_day = temp_buy
            sell_day = i

        if prices[i] < min_price:
            min_price = prices[i]
            temp_buy = i

    if best_profit == 0:
        return 0, -1, -1

    return best_profit, buy_day, sell_day


#  Test Cases 

# Test 1: Standard case -- buy low, sell high
assert max_profit([7, 1, 5, 3, 6, 4]) == 5

# Test 2: Decreasing prices -- no profit possible
assert max_profit([7, 6, 4, 3, 1]) == 0

# Test 3: Single element -- cannot buy and sell
assert max_profit([5]) == 0

# Test 4: Two elements -- profitable
assert max_profit([1, 5]) == 4

# Test 5: Two elements -- not profitable
assert max_profit([5, 1]) == 0

# Test 6: All same prices
assert max_profit([3, 3, 3, 3]) == 0

# Test 7: Min at beginning, max at end
assert max_profit([1, 2, 3, 4, 5]) == 4

# Test 8: Multiple valleys and peaks
assert max_profit([2, 4, 1, 7, 5, 3, 6]) == 6  # Buy at 1, sell at 7

# Test 9: Empty array
assert max_profit([]) == 0

# Test 10: Variant with day indices
profit, buy, sell = max_profit_with_days([7, 1, 5, 3, 6, 4])
assert profit == 5
assert buy == 1      # Buy on day 1 (price=1)
assert sell == 4     # Sell on day 4 (price=6)

# Test 11: No profit variant
profit, buy, sell = max_profit_with_days([7, 6, 4, 3, 1])
assert profit == 0
assert buy == -1
assert sell == -1

print("All test cases passed!")
