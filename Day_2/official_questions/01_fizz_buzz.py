def fizz_buzz(n):
    op=[]
    for i in range(1,n+1):
        if i%3==0 and i%5==0:
            op.append("FizzBuzz")
        elif   i%3==0:
            op.append("Fizz")
        elif    i%5==0:
            op.append("Buzz")
        else:
            op.append(str(i))
    return op

assert fizz_buzz(3)==["1","2","Fizz"]
assert fizz_buzz(15)==["1","2","Fizz","4","Buzz","Fizz","7","8","Fizz","Buzz","11","Fizz","13","14","FizzBuzz"]
print("all cases passed")