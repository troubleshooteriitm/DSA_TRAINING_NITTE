"""
Enterprise HR Hierarchy & Role Management System
===================================================
Corporate Use Case: Model an organization's HR hierarchy with
inheritance, encapsulation, polymorphism, and property decorators.

Features:
- Employee hierarchy: Employee  Manager  Executive
- Department management with budget tracking
- Role-based access control (RBAC)
- Org chart visualization
"""

from abc import ABC, abstractmethod
from datetime import datetime


# ============================================================
# BASE EMPLOYEE CLASS
# ============================================================

class Employee:
    """Base employee class with encapsulated salary."""

    _id_counter = 1000

    def __init__(self, name, department, salary, role="Staff"):
        Employee._id_counter += 1
        self._emp_id = f"EMP{Employee._id_counter}"
        self._name = name
        self._department = department
        self.__salary = salary  # Private
        self._role = role
        self._join_date = datetime.now().strftime("%Y-%m-%d")

    @property
    def emp_id(self):
        return self._emp_id

    @property
    def name(self):
        return self._name

    @property
    def department(self):
        return self._department

    @department.setter
    def department(self, value):
        if not value.strip():
            raise ValueError("Department cannot be empty")
        self._department = value

    @property
    def salary(self):
        return self.__salary

    @salary.setter
    def salary(self, value):
        if value < 0:
            raise ValueError("Salary cannot be negative")
        self.__salary = value

    @property
    def role(self):
        return self._role

    def get_annual_compensation(self):
        """Calculate annual compensation. Can be overridden."""
        return self.__salary * 12

    def __str__(self):
        return f"{self._emp_id} | {self._name:<20} | {self._role:<12} | {self._department:<15} | ₹{self.__salary:>10,.2f}"

    def __repr__(self):
        return f"Employee('{self._name}', '{self._department}', {self.__salary})"


# ============================================================
# MANAGER CLASS (INHERITANCE)
# ============================================================

class Manager(Employee):
    """Manager with direct reports."""

    def __init__(self, name, department, salary):
        super().__init__(name, department, salary, role="Manager")
        self._direct_reports = []

    def add_report(self, employee):
        """Add a direct report."""
        if employee not in self._direct_reports:
            self._direct_reports.append(employee)

    def remove_report(self, employee):
        """Remove a direct report."""
        self._direct_reports.remove(employee)

    @property
    def direct_reports(self):
        return self._direct_reports.copy()

    @property
    def team_size(self):
        return len(self._direct_reports)

    def get_annual_compensation(self):
        """Managers get a 10% management bonus."""
        base = super().get_annual_compensation()
        return base * 1.10  # 10% bonus


# ============================================================
# EXECUTIVE CLASS (MULTILEVEL INHERITANCE)
# ============================================================

class Executive(Manager):
    """Executive with stock options and bonus."""

    def __init__(self, name, department, salary, stock_options=0, annual_bonus=0):
        super().__init__(name, department, salary)
        self._role = "Executive"
        self._stock_options = stock_options
        self._annual_bonus = annual_bonus

    @property
    def stock_options(self):
        return self._stock_options

    def get_annual_compensation(self):
        """Executives get base + bonus + stock value estimate."""
        base = super().get_annual_compensation()
        return base + self._annual_bonus + (self._stock_options * 100)


# ============================================================
# DEPARTMENT CLASS (COMPOSITION)
# ============================================================

class Department:
    """Department with employees and budget management."""

    def __init__(self, name, budget):
        self._name = name
        self._budget = budget
        self._employees = []

    @property
    def name(self):
        return self._name

    @property
    def budget(self):
        return self._budget

    def add_employee(self, employee):
        self._employees.append(employee)
        employee.department = self._name

    def remove_employee(self, employee):
        self._employees.remove(employee)

    @property
    def headcount(self):
        return len(self._employees)

    @property
    def total_salary_cost(self):
        return sum(e.salary for e in self._employees)

    @property
    def budget_utilization(self):
        """Percentage of budget used for salaries."""
        if self._budget == 0:
            return 0
        return (self.total_salary_cost * 12 / self._budget) * 100

    def get_employees(self):
        return self._employees.copy()

    def __str__(self):
        return (f"Department: {self._name} | Headcount: {self.headcount} | "
                f"Budget: ₹{self._budget:,.2f} | Utilization: {self.budget_utilization:.1f}%")


# ============================================================
# ROLE-BASED ACCESS CONTROL (POLYMORPHISM + ABSTRACTION)
# ============================================================

class Permission(ABC):
    @abstractmethod
    def can_view_salary(self):
        pass

    @abstractmethod
    def can_approve_leave(self):
        pass

    @abstractmethod
    def can_hire(self):
        pass


class StaffPermission(Permission):
    def can_view_salary(self):
        return False  # Can only view own

    def can_approve_leave(self):
        return False

    def can_hire(self):
        return False


class ManagerPermission(Permission):
    def can_view_salary(self):
        return True  # Can view team's

    def can_approve_leave(self):
        return True

    def can_hire(self):
        return False


class ExecutivePermission(Permission):
    def can_view_salary(self):
        return True

    def can_approve_leave(self):
        return True

    def can_hire(self):
        return True


def get_permissions(employee):
    """Factory function -- returns permissions based on role."""
    role_map = {
        "Staff": StaffPermission(),
        "Manager": ManagerPermission(),
        "Executive": ExecutivePermission(),
    }
    return role_map.get(employee.role, StaffPermission())


# ============================================================
# ORG CHART DISPLAY
# ============================================================

def display_org_chart(manager, indent=0):
    """Display organization chart as a tree."""
    prefix = "  " * indent
    icon = "" if isinstance(manager, Executive) else "" if isinstance(manager, Manager) else ""
    print(f"{prefix}{icon} {manager.name} ({manager.role}, {manager.department})")

    if isinstance(manager, Manager):
        for report in manager.direct_reports:
            if isinstance(report, Manager):
                display_org_chart(report, indent + 1)
            else:
                prefix2 = "  " * (indent + 1)
                print(f"{prefix2} {report.name} ({report.role}, {report.department})")


# ============================================================
# DEMONSTRATION
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("   ENTERPRISE HR HIERARCHY & ROLE MANAGEMENT SYSTEM")
    print("=" * 70)

    # Create executives
    ceo = Executive("Rajesh Kumar", "Executive Office", 500000, stock_options=10000, annual_bonus=2000000)
    cto = Executive("Priya Sharma", "Engineering", 400000, stock_options=5000, annual_bonus=1000000)
    cfo = Executive("Amit Patel", "Finance", 380000, stock_options=4000, annual_bonus=900000)

    # Create managers
    eng_mgr1 = Manager("Sneha Reddy", "Engineering", 180000)
    eng_mgr2 = Manager("Vikram Singh", "Engineering", 175000)
    fin_mgr = Manager("Neha Gupta", "Finance", 160000)
    hr_mgr = Manager("Rahul Verma", "HR", 150000)

    # Create staff
    dev1 = Employee("Arun Kumar", "Engineering", 120000)
    dev2 = Employee("Meera Nair", "Engineering", 115000)
    dev3 = Employee("Karthik Iyer", "Engineering", 110000)
    dev4 = Employee("Divya Menon", "Engineering", 118000)
    analyst1 = Employee("Pooja Shah", "Finance", 95000)
    analyst2 = Employee("Suresh Babu", "Finance", 92000)
    hr1 = Employee("Anita Desai", "HR", 85000)
    hr2 = Employee("Ravi Teja", "HR", 82000)

    # Build hierarchy
    ceo.add_report(cto)
    ceo.add_report(cfo)
    ceo.add_report(hr_mgr)

    cto.add_report(eng_mgr1)
    cto.add_report(eng_mgr2)

    eng_mgr1.add_report(dev1)
    eng_mgr1.add_report(dev2)
    eng_mgr2.add_report(dev3)
    eng_mgr2.add_report(dev4)

    cfo.add_report(fin_mgr)
    fin_mgr.add_report(analyst1)
    fin_mgr.add_report(analyst2)

    hr_mgr.add_report(hr1)
    hr_mgr.add_report(hr2)

    # Create departments
    eng_dept = Department("Engineering", 50000000)
    for emp in [cto, eng_mgr1, eng_mgr2, dev1, dev2, dev3, dev4]:
        eng_dept.add_employee(emp)

    fin_dept = Department("Finance", 20000000)
    for emp in [cfo, fin_mgr, analyst1, analyst2]:
        fin_dept.add_employee(emp)

    hr_dept = Department("HR", 10000000)
    for emp in [hr_mgr, hr1, hr2]:
        hr_dept.add_employee(emp)

    # Display Org Chart
    print(f"\n{''*70}")
    print("   ORGANIZATION CHART")
    print(f"{''*70}")
    display_org_chart(ceo)

    # Employee Directory
    all_employees = [ceo, cto, cfo, eng_mgr1, eng_mgr2, fin_mgr, hr_mgr,
                     dev1, dev2, dev3, dev4, analyst1, analyst2, hr1, hr2]

    print(f"\n{''*70}")
    print("   EMPLOYEE DIRECTORY")
    print(f"{''*70}")
    print(f"  {'ID':<9} {'Name':<20} {'Role':<12} {'Department':<15} {'Salary':>12}")
    print(f"  {''*68}")
    for emp in all_employees:
        print(f"  {emp}")

    # Department Summary
    print(f"\n{''*70}")
    print("    DEPARTMENT SUMMARY")
    print(f"{''*70}")
    for dept in [eng_dept, fin_dept, hr_dept]:
        print(f"  {dept}")

    # Compensation Report
    print(f"\n{''*70}")
    print("   ANNUAL COMPENSATION (Polymorphism Demo)")
    print(f"{''*70}")
    for emp in [ceo, cto, eng_mgr1, dev1]:
        comp = emp.get_annual_compensation()
        print(f"  {emp.name:<20} ({emp.role:<10})  ₹{comp:>15,.2f}")

    # RBAC Demo
    print(f"\n{''*70}")
    print("   ROLE-BASED ACCESS CONTROL")
    print(f"{''*70}")
    for emp in [dev1, eng_mgr1, ceo]:
        perms = get_permissions(emp)
        print(f"  {emp.name:<20} ({emp.role:<10}): "
              f"View Salary={perms.can_view_salary()}, "
              f"Approve Leave={perms.can_approve_leave()}, "
              f"Hire={perms.can_hire()}")

    print(f"\n{'='*70}")
