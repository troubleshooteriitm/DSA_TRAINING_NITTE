# Day 6 -- Object-Oriented Programming (OOP)

##  Topics Covered
- Classes & Objects, Constructors
- Inheritance (Single, Multiple, Multilevel, MRO)
- Method Overriding, Encapsulation, Abstraction, Polymorphism
- Static & Class Methods, Property Decorators
- Magic/Dunder Methods

---

## 1. Classes and Objects

```python
class Car:
    """A simple Car class."""

    # Class variable (shared by all instances)
    total_cars = 0

    def __init__(self, brand, model, year):
        """Constructor -- called when object is created."""
        # Instance variables (unique to each object)
        self.brand = brand
        self.model = model
        self.year = year
        Car.total_cars += 1

    def display(self):
        """Instance method."""
        return f"{self.year} {self.brand} {self.model}"

# Creating objects (instantiation)
car1 = Car("Toyota", "Camry", 2023)
car2 = Car("Honda", "Civic", 2024)

print(car1.display())       # 2023 Toyota Camry
print(Car.total_cars)       # 2
```

---

## 2. Constructors -- `__init__` and `__new__`

```python
class Singleton:
    """__new__ controls object creation, __init__ initializes it."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.value = "I am singleton"

s1 = Singleton()
s2 = Singleton()
print(s1 is s2)  # True -- same object!
```

---

## 3. Inheritance

```python
# SINGLE INHERITANCE
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} makes a sound"

class Dog(Animal):
    def speak(self):  # Method overriding
        return f"{self.name} says Woof!"

# MULTILEVEL INHERITANCE
class Puppy(Dog):
    def play(self):
        return f"{self.name} is playing!"

# MULTIPLE INHERITANCE
class Flyable:
    def fly(self):
        return "I can fly!"

class Swimmable:
    def swim(self):
        return "I can swim!"

class Duck(Animal, Flyable, Swimmable):
    def speak(self):
        return f"{self.name} says Quack!"

duck = Duck("Donald")
print(duck.speak())   # Donald says Quack!
print(duck.fly())     # I can fly!
print(duck.swim())    # I can swim!

# MRO (Method Resolution Order)
print(Duck.__mro__)
# Duck -> Animal -> Flyable -> Swimmable -> object
```

---

## 4. Encapsulation

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner          # public
        self._account_type = "Savings"  # protected (convention)
        self.__balance = balance    # private (name mangling)

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            return True
        return False

    def get_balance(self):
        """Controlled access to private attribute."""
        return self.__balance

acc = BankAccount("Alice", 1000)
print(acc.owner)           # Alice -- public
print(acc._account_type)   # Savings -- accessible but "protected"
# print(acc.__balance)     # AttributeError!
print(acc.get_balance())   # 1000 -- via getter
print(acc._BankAccount__balance)  # 1000 -- name mangling (not recommended)
```

---

## 5. Abstraction (ABC Module)

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    """Abstract base class -- cannot be instantiated."""

    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def perimeter(self):
        pass

    def description(self):
        """Concrete method in abstract class."""
        return f"{self.__class__.__name__}: area={self.area():.2f}"

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        import math
        return math.pi * self.radius ** 2

    def perimeter(self):
        import math
        return 2 * math.pi * self.radius

# shape = Shape()  # TypeError: Can't instantiate abstract class!
rect = Rectangle(5, 3)
print(rect.description())  # Rectangle: area=15.00
```

---

## 6. Polymorphism

```python
# Duck typing -- "If it walks like a duck..."
class Cat:
    def speak(self):
        return "Meow"

class Dog:
    def speak(self):
        return "Woof"

class Duck:
    def speak(self):
        return "Quack"

# Same interface, different behavior
for animal in [Cat(), Dog(), Duck()]:
    print(animal.speak())

# Operator overloading (also polymorphism)
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(v1 + v2)  # Vector(4, 6)
```

---

## 7. Static & Class Methods

```python
class MathUtils:
    PI = 3.14159

    @staticmethod
    def add(a, b):
        """No access to cls or self. Pure utility."""
        return a + b

    @classmethod
    def circle_area(cls, radius):
        """Access class variables via cls."""
        return cls.PI * radius ** 2

    @classmethod
    def from_string(cls, data_string):
        """Alternative constructor pattern."""
        # Factory method
        return cls()

print(MathUtils.add(3, 5))         # 8
print(MathUtils.circle_area(5))    # 78.53975
```

---

## 8. Property Decorators

```python
class Temperature:
    def __init__(self, celsius=0):
        self._celsius = celsius

    @property
    def celsius(self):
        """Getter."""
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        """Setter with validation."""
        if value < -273.15:
            raise ValueError("Temperature below absolute zero!")
        self._celsius = value

    @property
    def fahrenheit(self):
        """Computed property."""
        return self._celsius * 9/5 + 32

temp = Temperature(25)
print(temp.celsius)      # 25
print(temp.fahrenheit)   # 77.0
temp.celsius = 100
print(temp.fahrenheit)   # 212.0
```

---

## 9. Magic/Dunder Methods

```python
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):          # print(), str()
        return f"{self.name}: ₹{self.price}"

    def __repr__(self):         # repr(), debugging
        return f"Product('{self.name}', {self.price})"

    def __len__(self):          # len()
        return len(self.name)

    def __eq__(self, other):    # ==
        return self.price == other.price

    def __lt__(self, other):    # <
        return self.price < other.price

    def __add__(self, other):   # +
        return self.price + other.price

    def __contains__(self, item):  # 'in' operator
        return item.lower() in self.name.lower()

p1 = Product("Laptop", 75000)
p2 = Product("Mouse", 500)

print(str(p1))          # Laptop: ₹75000
print(repr(p1))         # Product('Laptop', 75000)
print(len(p1))          # 6
print(p1 == p2)         # False
print(p1 > p2)          # True
print(p1 + p2)          # 75500
print("lap" in p1)      # True
```

---

##  Interview Tips
- **SOLID Principles**: Know Single Responsibility, Open/Closed, Liskov Substitution
- **Composition vs Inheritance**: "Has-a" vs "Is-a" -- prefer composition
- **MRO**: Python uses C3 linearization. Use `ClassName.__mro__` to check
- **`super()`**: Always use `super()` instead of parent class name directly
- **`@property`**: Preferred over getter/setter methods in Python

##  Practice Problems
| Problem | Platform | Difficulty |
|---------|----------|------------|
| Design Parking System | LeetCode 1603 | Easy |
| Merge Intervals | LeetCode 56 | Medium |
| Classes and Objects | HackerRank | Easy |
