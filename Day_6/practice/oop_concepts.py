"""
OOP Concepts Practice
======================
Hands-on examples: class creation, inheritance hierarchy, method overriding, encapsulation.
"""

from abc import ABC, abstractmethod

# ============================================================
# 1. BASIC CLASS
# ============================================================

class Student:
    """A student with grades."""
    def __init__(self, name, grades=None):
        self.name = name
        self.grades = grades or []

    def add_grade(self, grade):
        self.grades.append(grade)

    @property
    def average(self):
        return sum(self.grades) / len(self.grades) if self.grades else 0

    @property
    def gpa(self):
        avg = self.average
        if avg >= 90: return "A+"
        elif avg >= 80: return "A"
        elif avg >= 70: return "B"
        elif avg >= 60: return "C"
        else: return "F"

    def __str__(self):
        return f"{self.name}: avg={self.average:.1f} ({self.gpa})"


# ============================================================
# 2. INHERITANCE HIERARCHY
# ============================================================

class Vehicle(ABC):
    """Abstract vehicle base class."""
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year

    @abstractmethod
    def fuel_type(self):
        pass

    def __str__(self):
        return f"{self.year} {self.brand} {self.model} ({self.fuel_type()})"


class ElectricCar(Vehicle):
    def __init__(self, brand, model, year, battery_kwh):
        super().__init__(brand, model, year)
        self.battery_kwh = battery_kwh

    def fuel_type(self):
        return f"Electric - {self.battery_kwh}kWh"


class PetrolCar(Vehicle):
    def __init__(self, brand, model, year, engine_cc):
        super().__init__(brand, model, year)
        self.engine_cc = engine_cc

    def fuel_type(self):
        return f"Petrol - {self.engine_cc}cc"


class HybridCar(ElectricCar, PetrolCar):
    """Multiple inheritance -- hybrid car."""
    def __init__(self, brand, model, year, battery_kwh, engine_cc):
        # Using super() with MRO
        Vehicle.__init__(self, brand, model, year)
        self.battery_kwh = battery_kwh
        self.engine_cc = engine_cc

    def fuel_type(self):
        return f"Hybrid - {self.battery_kwh}kWh + {self.engine_cc}cc"


# ============================================================
# 3. ENCAPSULATION WITH VALIDATION
# ============================================================

class BankAccount:
    """Bank account with controlled access."""
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.__balance = balance
        self.__transactions = []

    @property
    def balance(self):
        return self.__balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self.__balance += amount
        self.__transactions.append(f"+₹{amount:,.2f}")

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal must be positive")
        if amount > self.__balance:
            raise ValueError("Insufficient funds")
        self.__balance -= amount
        self.__transactions.append(f"-₹{amount:,.2f}")

    def get_statement(self):
        return self.__transactions.copy()


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":
    print("=" * 50)
    print("  OOP CONCEPTS PRACTICE")
    print("=" * 50)

    # Students
    print("\n--- Student Grades ---")
    s1 = Student("Alice", [92, 88, 95, 90])
    s2 = Student("Bob", [65, 72, 58, 70])
    print(s1)
    print(s2)

    # Vehicles (polymorphism)
    print("\n--- Vehicle Hierarchy ---")
    vehicles = [
        ElectricCar("Tesla", "Model 3", 2024, 75),
        PetrolCar("Toyota", "Camry", 2023, 2500),
        HybridCar("Toyota", "Prius", 2024, 8.8, 1800),
    ]
    for v in vehicles:
        print(f"  {v}")

    print(f"\n  MRO of HybridCar: {[c.__name__ for c in HybridCar.__mro__]}")

    # Bank Account (encapsulation)
    print("\n--- Bank Account ---")
    acc = BankAccount("Alice", 10000)
    acc.deposit(5000)
    acc.withdraw(3000)
    acc.deposit(2000)
    print(f"  Balance: ₹{acc.balance:,.2f}")
    print(f"  Transactions: {acc.get_statement()}")
