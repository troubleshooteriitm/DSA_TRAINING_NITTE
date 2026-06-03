
def validate_employee_data(employee):
	"""
	Validates employee data dictionary.
	Required fields: name (str), employee_id (str/int), email (str), age (int)
	Returns: (bool, list of error messages)
	"""
	import re
	errors = []
	# Name validation
	name = employee.get('name', '').strip()
	if not name:
		errors.append('Name is required.')
	# Employee ID validation
	emp_id = employee.get('employee_id')
	if not emp_id or (isinstance(emp_id, str) and not emp_id.strip()):
		errors.append('Employee ID is required.')
	# Email validation
	email = employee.get('email', '').strip()
	email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
	if not email or not re.match(email_pattern, email):
		errors.append('Valid email is required.')
	# Age validation
	age = employee.get('age')
	try:
		age = int(age)
		if age < 18 or age > 70:
			errors.append('Age must be between 18 and 70.')
	except (TypeError, ValueError):
		errors.append('Valid age is required.')
	return (len(errors) == 0, errors)


# Example usage
if __name__ == "__main__":
	sample_employee = {
		'name': 'Alice Smith',
		'employee_id': 'E123',
		'email': 'alice.smith@example.com',
		'age': 30
	}
	is_valid, error_list = validate_employee_data(sample_employee)
	if is_valid:
		print("Employee data is valid.")
	else:
		print("Employee data is invalid:")
		for err in error_list:
			print("-", err)

