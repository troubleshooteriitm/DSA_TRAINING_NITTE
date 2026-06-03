class Person:
    def __init__(self, name, age=20):# constructor
        self.name = name
        self.age = age

    def greet(self):
        return f"Hello, my name is {self.name} and I am {self.age} years old."
