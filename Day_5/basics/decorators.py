def changecase(func):
  print("Inside the decorator")
  def myinner():
    print("Inside the inner function")
    return func().strip()
  return myinner


@changecase
def myfunction():
  print("Inside the myfunction")
  return "Hello Sally        "

print(myfunction())