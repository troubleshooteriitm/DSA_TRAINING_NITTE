def valid_palindrome(str):
    cleaned=""
    for char in str:
        if char ==" ":
            continue
        elif char.isalnum():
            cleaned+=char.lower()

    return cleaned==cleaned[::-1]

assert valid_palindrome("Was it a car or a cat I saw?")==True

print("All passed")