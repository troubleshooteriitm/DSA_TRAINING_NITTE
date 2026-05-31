"""
Enterprise Validation Framework
================================
A reusable validation framework used across multiple internal portals.
Demonstrates: decorators, *args/**kwargs, lambda, map/filter, function composition.

Corporate Use Case:
    Multiple internal portals (HR, Sales, Support) need consistent data
    validation. Instead of duplicating logic, this framework provides
    composable validators that can be reused across all portals.
"""

from functools import reduce
import re
from datetime import datetime


# ============================================================
# CORE VALIDATOR DECORATORS
# ============================================================

def validator(error_message):
    """Decorator factory to create named validators with error messages."""
    def decorator(func):
        func.error_message = error_message
        func.is_validator = True
        return func
    return decorator


def required_field(field_name):
    """Validator: checks that a field is present and non-empty."""
    @validator(f"'{field_name}' is required and cannot be empty.")
    def validate(data):
        value = data.get(field_name)
        if value is None or (isinstance(value, str) and not value.strip()):
            return False
        return True
    validate.__name__ = f"required_{field_name}"
    return validate


def email_validator(field_name="email"):
    """Validator: checks that the field contains a valid email address."""
    pattern = r"^[\w\.\-\+]+@[\w\.\-]+\.\w{2,}$"

    @validator(f"'{field_name}' must be a valid email address.")
    def validate(data):
        email = data.get(field_name, "")
        return bool(re.match(pattern, str(email).strip()))
    validate.__name__ = f"email_{field_name}"
    return validate


def phone_validator(field_name="phone"):
    """Validator: checks that the field contains a valid phone number."""
    pattern = r"^\+?[\d\s\-\(\)]{7,15}$"

    @validator(f"'{field_name}' must be a valid phone number.")
    def validate(data):
        phone = data.get(field_name, "")
        return bool(re.match(pattern, str(phone).strip()))
    validate.__name__ = f"phone_{field_name}"
    return validate


def age_range_validator(field_name="age", min_age=18, max_age=65):
    """Validator: checks that age is within the specified range."""
    @validator(f"'{field_name}' must be between {min_age} and {max_age}.")
    def validate(data):
        try:
            age = int(data.get(field_name, 0))
            return min_age <= age <= max_age
        except (TypeError, ValueError):
            return False
    validate.__name__ = f"age_range_{field_name}"
    return validate


def regex_pattern_validator(field_name, pattern, description=""):
    """Validator: checks that the field matches a custom regex pattern."""
    msg = f"'{field_name}' does not match required format"
    if description:
        msg += f" ({description})"

    @validator(msg + ".")
    def validate(data):
        value = data.get(field_name, "")
        return bool(re.match(pattern, str(value).strip()))
    validate.__name__ = f"regex_{field_name}"
    return validate


def min_length_validator(field_name, min_len):
    """Validator: checks that the field has a minimum length."""
    @validator(f"'{field_name}' must be at least {min_len} characters long.")
    def validate(data):
        value = data.get(field_name, "")
        return len(str(value).strip()) >= min_len
    validate.__name__ = f"min_length_{field_name}"
    return validate


def date_validator(field_name, fmt="%Y-%m-%d"):
    """Validator: checks that the field is a valid date in the given format."""
    @validator(f"'{field_name}' must be a valid date in format '{fmt}'.")
    def validate(data):
        try:
            datetime.strptime(str(data.get(field_name, "")), fmt)
            return True
        except ValueError:
            return False
    validate.__name__ = f"date_{field_name}"
    return validate


# ============================================================
# VALIDATOR COMPOSITION
# ============================================================

def compose_validators(*validators):
    """
    Compose multiple validators into a single validation function.
    Returns a function that takes data and returns (is_valid, errors).

    Uses reduce and lambda to chain validators -- demonstrating
    functional programming in a real enterprise context.
    """
    def validate(data):
        results = list(map(lambda v: (v(data), v.error_message), validators))
        errors = list(
            map(
                lambda r: r[1],
                filter(lambda r: not r[0], results)
            )
        )
        is_valid = reduce(lambda a, b: a and b[0], results, True)
        return is_valid, errors
    return validate


# ============================================================
# PORTAL-SPECIFIC VALIDATORS
# ============================================================

# HR Portal -- Employee Registration Form
hr_employee_validator = compose_validators(
    required_field("name"),
    required_field("employee_id"),
    email_validator("email"),
    phone_validator("phone"),
    age_range_validator("age", min_age=18, max_age=70),
    regex_pattern_validator("employee_id", r"^EMP\d{4,6}$", "EMP followed by 4-6 digits"),
    date_validator("join_date"),
)

# Sales Portal -- Customer Registration Form
sales_customer_validator = compose_validators(
    required_field("company_name"),
    required_field("contact_person"),
    email_validator("contact_email"),
    phone_validator("contact_phone"),
    regex_pattern_validator("gst_number", r"^\d{2}[A-Z]{5}\d{4}[A-Z]\d[Z][A-Z\d]$", "valid GST number"),
)

# Support Portal -- Ticket Submission Form
support_ticket_validator = compose_validators(
    required_field("title"),
    required_field("description"),
    required_field("priority"),
    email_validator("reporter_email"),
    min_length_validator("description", 20),
)


# ============================================================
# DEMONSTRATION
# ============================================================

def print_validation_result(form_name, data, is_valid, errors):
    """Pretty-print validation results."""
    print(f"\n{'='*60}")
    print(f"  {form_name}")
    print(f"{'='*60}")
    print(f"  Data: {data}")
    if is_valid:
        print(f"  [PASS] Result: VALID")
    else:
        print(f"  [FAIL] Result: INVALID")
        for err in errors:
            print(f"     - {err}")


if __name__ == "__main__":
    print("=" * 60)
    print("  ENTERPRISE VALIDATION FRAMEWORK DEMO")
    print("=" * 60)

    # --- HR Portal Tests ---
    valid_employee = {
        "name": "Priya Sharma",
        "employee_id": "EMP10234",
        "email": "priya.sharma@company.com",
        "phone": "+91-9876543210",
        "age": 28,
        "join_date": "2025-03-15",
    }
    is_valid, errors = hr_employee_validator(valid_employee)
    print_validation_result("HR Portal -- Valid Employee", valid_employee, is_valid, errors)

    invalid_employee = {
        "name": "",
        "employee_id": "INVALID",
        "email": "not-an-email",
        "phone": "123",
        "age": 15,
        "join_date": "March 2025",
    }
    is_valid, errors = hr_employee_validator(invalid_employee)
    print_validation_result("HR Portal -- Invalid Employee", invalid_employee, is_valid, errors)

    # --- Sales Portal Tests ---
    valid_customer = {
        "company_name": "TechCorp Solutions",
        "contact_person": "Rahul Verma",
        "contact_email": "rahul@techcorp.in",
        "contact_phone": "+91-9123456789",
        "gst_number": "29ABCDE1234F1Z5",
    }
    is_valid, errors = sales_customer_validator(valid_customer)
    print_validation_result("Sales Portal -- Valid Customer", valid_customer, is_valid, errors)

    invalid_customer = {
        "company_name": "",
        "contact_person": "Rahul",
        "contact_email": "bad-email",
        "contact_phone": "123",
        "gst_number": "INVALID",
    }
    is_valid, errors = sales_customer_validator(invalid_customer)
    print_validation_result("Sales Portal -- Invalid Customer", invalid_customer, is_valid, errors)

    # --- Support Portal Tests ---
    valid_ticket = {
        "title": "Login page not loading",
        "description": "The login page shows a blank white screen after the latest deployment on May 30th.",
        "priority": "High",
        "reporter_email": "user@company.com",
    }
    is_valid, errors = support_ticket_validator(valid_ticket)
    print_validation_result("Support Portal -- Valid Ticket", valid_ticket, is_valid, errors)

    invalid_ticket = {
        "title": "",
        "description": "Help",
        "priority": "",
        "reporter_email": "not-email",
    }
    is_valid, errors = support_ticket_validator(invalid_ticket)
    print_validation_result("Support Portal -- Invalid Ticket", invalid_ticket, is_valid, errors)

    print(f"\n{'='*60}")
    print("  Framework supports any portal via compose_validators()!")
    print(f"{'='*60}")
