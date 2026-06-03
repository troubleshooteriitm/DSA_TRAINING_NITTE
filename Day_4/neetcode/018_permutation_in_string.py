def checkInclusion(s1,s2):
    if len(s1) > len(s2):
            return False

    target = [0] * 26 # [0,0,0,0,..]for a-z
    window = [0] * 26 # [0,0,0,0,..]for a-z
    
    for c in s1:
        target[ord(c) - ord('a')] += 1
    print("line 9 ",target[:15])
    for i in range(len(s1)):
        window[ord(s2[i]) - ord('a')] += 1
    print("line 12",window[:15])
    if target == window:
        return True

    for i in range(len(s1), len(s2)): # 3,4,5,6
        window[ord(s2[i]) - ord('a')] += 1
        print("line 18",window[:15])
        window[ord(s2[i - len(s1)]) - ord('a')] -= 1
        print("line 20",window[:15])
        print("line 21",i,target[:15])
        if target == window:
            return True

    return False

assert checkInclusion("abc", "lecabee") == True
# assert checkInclusion("abc", "lecaabee") == False
print("all pass")