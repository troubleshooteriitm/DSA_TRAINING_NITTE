class Parent:
    def __init__(self, name, age, password):
        self.name = name
        self._age = age # Protected property
        self.__password = password # Private property

class Child(Parent):
    def __init__(self, name, age, password):
        super().__init__(name, age, password)

    def display_info(self):
        print(f"Name: {self.name}")
        print(f"Age: {self._age}") # Accessing protected property
        print(f"Password: {self.__password}") # This will cause an error





