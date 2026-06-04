try:
    x=10
    y=0
    print(x/y)
except ZeroDivisionError as e:
    print(e)
finally:
    print("This will always execute")