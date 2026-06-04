class AgeError(Exception):
    pass

try:
    age=17
    if age>18:
        print("allowed!!")
    else:
        raise AgeError("come back when you turn 18")
except Exception as e:
    print(e)

print("I am IronMan!!!")