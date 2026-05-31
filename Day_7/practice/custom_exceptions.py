"""
Custom Exceptions -- Practice Examples

This module demonstrates:
1. Creating a hierarchy of custom exceptions
2. Adding custom attributes and methods to exceptions
3. Using custom exceptions in business logic
4. Exception chaining and context

Topics Covered:
- Inheriting from Exception
- Building exception hierarchies
- Custom __init__ and __str__
- Using 'raise ... from ...' for exception chaining
- Practical business logic examples
"""


# ============================================================
# 1. Basic Custom Exception
# ============================================================

class ApplicationError(Exception):
    """
    Base exception for the entire application.

    All custom exceptions should inherit from this class,
    allowing callers to catch all app-specific errors with
    a single except clause if desired.
    """
    pass


# ============================================================
# 2. Exception Hierarchy -- E-Commerce Domain
# ============================================================

class OrderError(ApplicationError):
    """Base exception for order-related errors."""
    pass


class OutOfStockError(OrderError):
    """Raised when a product is out of stock."""

    def __init__(self, product_name: str, requested_qty: int,
                 available_qty: int):
        self.product_name = product_name
        self.requested_qty = requested_qty
        self.available_qty = available_qty
        super().__init__(
            f"'{product_name}' is out of stock. "
            f"Requested: {requested_qty}, Available: {available_qty}"
        )


class InvalidCouponError(OrderError):
    """Raised when an invalid or expired coupon is applied."""

    def __init__(self, coupon_code: str, reason: str = "Invalid coupon"):
        self.coupon_code = coupon_code
        self.reason = reason
        super().__init__(f"Coupon '{coupon_code}': {reason}")


class PaymentError(OrderError):
    """Base exception for payment-related errors."""
    pass


class PaymentDeclinedError(PaymentError):
    """Raised when a payment is declined by the gateway."""

    def __init__(self, amount: float, reason: str = "Card declined"):
        self.amount = amount
        self.reason = reason
        super().__init__(
            f"Payment of ₹{amount:,.2f} declined: {reason}"
        )


class PaymentTimeoutError(PaymentError):
    """Raised when a payment request times out."""

    def __init__(self, timeout_seconds: int):
        self.timeout_seconds = timeout_seconds
        super().__init__(
            f"Payment gateway timed out after {timeout_seconds} seconds"
        )


# ============================================================
# 3. Exception Hierarchy -- User Authentication Domain
# ============================================================

class AuthenticationError(ApplicationError):
    """Base exception for authentication errors."""
    pass


class InvalidCredentialsError(AuthenticationError):
    """Raised when login credentials are incorrect."""

    def __init__(self, username: str):
        self.username = username
        # NOTE: Never include the password in error messages!
        super().__init__(f"Invalid credentials for user '{username}'")


class AccountLockedError(AuthenticationError):
    """Raised when an account is locked due to too many failed attempts."""

    def __init__(self, username: str, lock_duration_minutes: int):
        self.username = username
        self.lock_duration_minutes = lock_duration_minutes
        super().__init__(
            f"Account '{username}' is locked for "
            f"{lock_duration_minutes} minutes"
        )


class SessionExpiredError(AuthenticationError):
    """Raised when a user's session has expired."""

    def __init__(self, session_id: str):
        self.session_id = session_id
        super().__init__(f"Session '{session_id[:8]}...' has expired")


# ============================================================
# 4. Business Logic -- E-Commerce Store
# ============================================================

class Product:
    """Simple product with name, price, and stock."""

    def __init__(self, name: str, price: float, stock: int):
        self.name = name
        self.price = price
        self.stock = stock

    def __repr__(self) -> str:
        return f"Product({self.name!r}, price=₹{self.price}, stock={self.stock})"


class ShoppingCart:
    """
    Shopping cart that uses custom exceptions for error handling.
    """

    # Valid coupon codes and their discount percentages
    VALID_COUPONS = {
        "SAVE10": 10,
        "SAVE20": 20,
        "WELCOME": 15,
    }

    def __init__(self):
        self.items: list[tuple[Product, int]] = []  # (product, quantity)
        self.discount_percent = 0
        self.coupon_applied: str | None = None

    def add_item(self, product: Product, quantity: int) -> None:
        """
        Add a product to the cart.

        Raises:
            OutOfStockError: If requested quantity exceeds available stock.
            ValueError: If quantity is not positive.
        """
        if quantity <= 0:
            raise ValueError(f"Quantity must be positive, got {quantity}")

        if quantity > product.stock:
            raise OutOfStockError(product.name, quantity, product.stock)

        self.items.append((product, quantity))
        print(f"  Added {quantity}x {product.name} to cart.")

    def apply_coupon(self, coupon_code: str) -> None:
        """
        Apply a discount coupon.

        Raises:
            InvalidCouponError: If the coupon code is not valid.
        """
        coupon_code = coupon_code.upper()

        if self.coupon_applied:
            raise InvalidCouponError(
                coupon_code, "A coupon has already been applied"
            )

        if coupon_code not in self.VALID_COUPONS:
            raise InvalidCouponError(coupon_code, "Coupon code not recognized")

        self.discount_percent = self.VALID_COUPONS[coupon_code]
        self.coupon_applied = coupon_code
        print(f"  Coupon '{coupon_code}' applied -- {self.discount_percent}% off!")

    def calculate_total(self) -> float:
        """Calculate the total price after discount."""
        subtotal = sum(product.price * qty for product, qty in self.items)
        discount = subtotal * (self.discount_percent / 100)
        return subtotal - discount

    def checkout(self, payment_amount: float) -> None:
        """
        Process checkout.

        Raises:
            PaymentDeclinedError: If payment amount doesn't match total.
        """
        total = self.calculate_total()

        if payment_amount < total:
            raise PaymentDeclinedError(
                payment_amount,
                f"Insufficient payment. Total is ₹{total:,.2f}"
            )

        # Deduct stock
        for product, qty in self.items:
            product.stock -= qty

        print(f"   Checkout successful! Total: ₹{total:,.2f}")


# ============================================================
# 5. Business Logic -- Authentication System
# ============================================================

class AuthSystem:
    """
    Simple authentication system demonstrating custom exceptions.
    """

    MAX_ATTEMPTS = 3
    LOCK_DURATION = 15  # minutes

    def __init__(self):
        # username -> password (in real systems, use hashed passwords!)
        self._users = {
            "alice": "password123",
            "bob": "securepass",
            "charlie": "mypassword",
        }
        # Track failed attempts per user
        self._failed_attempts: dict[str, int] = {}
        # Track locked accounts
        self._locked_accounts: set[str] = set()
        # Active sessions
        self._sessions: dict[str, str] = {}  # session_id -> username

    def login(self, username: str, password: str) -> str:
        """
        Authenticate a user and return a session ID.

        Raises:
            AccountLockedError: If the account is locked.
            InvalidCredentialsError: If credentials are wrong.
        """
        # Check if account is locked
        if username in self._locked_accounts:
            raise AccountLockedError(username, self.LOCK_DURATION)

        # Check if user exists and password matches
        if username not in self._users or self._users[username] != password:
            # Track failed attempt
            self._failed_attempts[username] = (
                self._failed_attempts.get(username, 0) + 1
            )

            # Lock account if max attempts exceeded
            if self._failed_attempts[username] >= self.MAX_ATTEMPTS:
                self._locked_accounts.add(username)
                raise AccountLockedError(username, self.LOCK_DURATION)

            raise InvalidCredentialsError(username)

        # Successful login -- reset failed attempts and create session
        self._failed_attempts[username] = 0
        session_id = f"sess-{username}-{id(self)}"
        self._sessions[session_id] = username
        print(f"   Login successful for '{username}'")
        return session_id

    def validate_session(self, session_id: str) -> str:
        """
        Validate a session ID and return the associated username.

        Raises:
            SessionExpiredError: If the session is not found / expired.
        """
        if session_id not in self._sessions:
            raise SessionExpiredError(session_id)

        return self._sessions[session_id]


# ============================================================
# 6. Exception Chaining Example
# ============================================================

class DataProcessingError(ApplicationError):
    """Raised when data processing fails."""
    pass


def load_configuration(filepath: str) -> dict:
    """
    Demonstrates exception chaining with 'raise ... from ...'.

    Raises:
        DataProcessingError: Wrapping the original FileNotFoundError.
    """
    try:
        with open(filepath, 'r') as f:
            return eval(f.read())  # Simplified; use json.load() in practice
    except FileNotFoundError as e:
        # Chain the original exception for full traceback context
        raise DataProcessingError(
            f"Configuration file '{filepath}' could not be loaded"
        ) from e
    except SyntaxError as e:
        raise DataProcessingError(
            f"Configuration file '{filepath}' has invalid syntax"
        ) from e


# ============================================================
# Main -- Demonstrate All Examples
# ============================================================

def main():
    """Run all demonstration examples."""

    print("=" * 60)
    print("  CUSTOM EXCEPTIONS -- DEMONSTRATION")
    print("=" * 60)

    # --- E-Commerce Examples ---
    print("\n--- E-Commerce: Shopping Cart ---\n")

    # Create products
    laptop = Product("Laptop", 75_000.00, 5)
    mouse = Product("Wireless Mouse", 1_500.00, 2)
    keyboard = Product("Mechanical Keyboard", 8_000.00, 0)  # Out of stock!

    cart = ShoppingCart()

    # Add items -- some will succeed, some will fail
    try:
        cart.add_item(laptop, 1)
    except OutOfStockError as e:
        print(f"   {e}")

    try:
        cart.add_item(mouse, 1)
    except OutOfStockError as e:
        print(f"   {e}")

    # This should fail -- keyboard is out of stock
    try:
        cart.add_item(keyboard, 1)
    except OutOfStockError as e:
        print(f"   {e}")
        print(f"     Available: {e.available_qty}, Requested: {e.requested_qty}")

    # Apply a valid coupon
    try:
        cart.apply_coupon("SAVE10")
    except InvalidCouponError as e:
        print(f"   {e}")

    # Try applying a second coupon -- should fail
    try:
        cart.apply_coupon("WELCOME")
    except InvalidCouponError as e:
        print(f"   {e}")

    # Try an invalid coupon
    try:
        cart2 = ShoppingCart()
        cart2.add_item(laptop, 1)
        cart2.apply_coupon("FAKECODE")
    except InvalidCouponError as e:
        print(f"   {e}")

    # Checkout with sufficient payment
    try:
        total = cart.calculate_total()
        print(f"\n  Cart total: ₹{total:,.2f}")
        cart.checkout(total)
    except PaymentDeclinedError as e:
        print(f"   {e}")

    # --- Authentication Examples ---
    print("\n--- Authentication System ---\n")

    auth = AuthSystem()

    # Successful login
    try:
        session = auth.login("alice", "password123")
    except (InvalidCredentialsError, AccountLockedError) as e:
        print(f"   {e}")

    # Failed login attempts leading to account lock
    for attempt in range(1, 5):
        try:
            auth.login("bob", "wrongpassword")
        except InvalidCredentialsError as e:
            print(f"   Attempt {attempt}: {e}")
        except AccountLockedError as e:
            print(f"   Attempt {attempt}: {e}")
            break

    # Validate a session
    try:
        user = auth.validate_session("invalid-session-id")
    except SessionExpiredError as e:
        print(f"   {e}")

    # --- Exception Chaining Example ---
    print("\n--- Exception Chaining ---\n")

    try:
        config = load_configuration("nonexistent_config.yaml")
    except DataProcessingError as e:
        print(f"   {e}")
        if e.__cause__:
            print(f"     Original cause: {e.__cause__}")

    # --- Catching at Different Hierarchy Levels ---
    print("\n--- Catching by Hierarchy Level ---\n")

    exceptions_to_test = [
        OutOfStockError("Widget", 10, 0),
        PaymentDeclinedError(1000, "Card expired"),
        InvalidCredentialsError("testuser"),
        AccountLockedError("testuser", 15),
    ]

    for exc in exceptions_to_test:
        try:
            raise exc
        except PaymentError as e:
            # Catches PaymentDeclinedError, PaymentTimeoutError
            print(f"  [PaymentError]        {e}")
        except OrderError as e:
            # Catches OutOfStockError, InvalidCouponError
            print(f"  [OrderError]          {e}")
        except AuthenticationError as e:
            # Catches InvalidCredentialsError, AccountLockedError,
            # SessionExpiredError
            print(f"  [AuthenticationError] {e}")
        except ApplicationError as e:
            # Catches anything else from our hierarchy
            print(f"  [ApplicationError]    {e}")

    print("\n" + "=" * 60)
    print("  ALL DEMONSTRATIONS COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
