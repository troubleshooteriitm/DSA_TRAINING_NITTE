from .Person import Person

class Student(Person):
    def __init__(self,roll_number,Class,Department):
        self.roll_number=roll_number
        self.Class=Class
        self.Department=Department


