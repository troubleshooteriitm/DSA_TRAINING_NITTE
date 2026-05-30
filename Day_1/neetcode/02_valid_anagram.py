from collections import Counter
def valid_anagram(str1,str2):
    return Counter(str1)==Counter(str2)


assert  valid_anagram("eebb","bbee")==True
assert valid_anagram("race","care")==True
assert valid_anagram("apple","stevejobs")==False
print("all cases passed")