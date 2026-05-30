def is_palindrome(string):
    return string==string[::-1]


assert is_palindrome("abcd")==False
assert is_palindrome("malayalam")==True
print("all cases passed")