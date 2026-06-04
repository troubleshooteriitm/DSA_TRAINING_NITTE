def dailytemperatures(temperatures):
    res = [0] * len(temperatures)
    stack = []  # pair: [temp, index]

    for i, t in enumerate(temperatures):
        print(i,t,stack,res)
        while stack and t > stack[-1][0]:
            stackT, stackInd = stack.pop()
            res[stackInd] = i - stackInd
        stack.append((t, i))
    return res


assert dailytemperatures([30,38,30,36,35,40,28])==[1,4,1,2,1,0,0]