def get_fullname_employee(employee):
    full_name = []
    if employee.first_name:
        full_name.append(employee.first_name)

    if employee.middle_name:
        full_name.append(employee.middle_name)

    if employee.last_name:
        full_name.append(employee.last_name)

    return " ".join(full_name)
