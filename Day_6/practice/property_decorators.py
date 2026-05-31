"""
Property Decorators Practice
==============================
Examples: temperature converter, bank account validation, user profile.
"""


class Temperature:
    """Temperature with auto-conversion between Celsius and Fahrenheit."""

    def __init__(self, celsius=0):
        self._celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Temperature below absolute zero (-273.15°C)!")
        self._celsius = value

    @property
    def fahrenheit(self):
        return round(self._celsius * 9 / 5 + 32, 2)

    @fahrenheit.setter
    def fahrenheit(self, value):
        self.celsius = round((value - 32) * 5 / 9, 2)

    @property
    def kelvin(self):
        return round(self._celsius + 273.15, 2)

    def __str__(self):
        return f"{self._celsius}°C = {self.fahrenheit}°F = {self.kelvin}K"


class SmartBankAccount:
    """Bank account with property-based validation."""

    def __init__(self, owner, balance=0, min_balance=1000):
        self._owner = owner
        self._balance = balance
        self._min_balance = min_balance

    @property
    def owner(self):
        return self._owner

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        if value < self._min_balance:
            raise ValueError(
                f"Balance cannot go below ₹{self._min_balance:,.2f}. "
                f"Attempted: ₹{value:,.2f}"
            )
        self._balance = value

    @property
    def is_premium(self):
        """Computed property -- premium if balance > 100,000."""
        return self._balance > 100000

    @property
    def account_type(self):
        if self._balance > 1000000:
            return "Platinum"
        elif self._balance > 100000:
            return "Gold"
        elif self._balance > 10000:
            return "Silver"
        return "Basic"

    def __str__(self):
        return (f"Account({self._owner}) | ₹{self._balance:,.2f} | "
                f"{self.account_type} | Premium: {self.is_premium}")


class UserProfile:
    """User profile with email and age validation."""

    def __init__(self, name, email, age):
        self.name = name
        self.email = email  # Uses setter
        self.age = age      # Uses setter

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value or not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value.strip().title()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        import re
        if not re.match(r"^[\w\.\-]+@[\w\.\-]+\.\w+$", value):
            raise ValueError(f"Invalid email: {value}")
        self._email = value.lower()

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if not isinstance(value, int) or value < 0 or value > 150:
            raise ValueError(f"Invalid age: {value}")
        self._age = value

    @age.deleter
    def age(self):
        print("Age information deleted for privacy")
        self._age = None

    def __str__(self):
        return f"User({self._name}, {self._email}, age={self._age})"


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":
    print("=" * 50)
    print("  PROPERTY DECORATORS PRACTICE")
    print("=" * 50)

    # Temperature
    print("\n--- Temperature Converter ---")
    t = Temperature(100)
    print(f"  {t}")
    t.fahrenheit = 72
    print(f"  Set to 72°F: {t}")
    t.celsius = 0
    print(f"  Set to 0°C: {t}")

    # Bank Account
    print("\n--- Smart Bank Account ---")
    acc = SmartBankAccount("Alice", 50000)
    print(f"  {acc}")
    acc.balance = 150000
    print(f"  After deposit: {acc}")
    try:
        acc.balance = 500  # Below minimum
    except ValueError as e:
        print(f"  Error: {e}")

    # User Profile
    print("\n--- User Profile ---")
    user = UserProfile("alice smith", "Alice.Smith@Gmail.COM", 28)
    print(f"  {user}")
    user.name = "bob jones"
    print(f"  Name changed: {user}")
    try:
        user.email = "invalid"
    except ValueError as e:
        print(f"  Error: {e}")

    # Deleter
    del user.age
    print(f"  After deleting age: {user}")
