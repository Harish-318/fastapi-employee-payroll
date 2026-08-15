from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import models
import schemas


# ============================================================
# DEPARTMENT CRUD
# ============================================================

def create_department(
    db: Session,
    department: schemas.DepartmentCreate
):
    existing_department = (
        db.query(models.Department)
        .filter(models.Department.name == department.name)
        .first()
    )

    if existing_department:
        raise ValueError("Department with this name already exists.")

    new_department = models.Department(
        name=department.name,
        manager_name=department.manager_name
    )

    db.add(new_department)
    db.commit()
    db.refresh(new_department)

    return new_department


def get_departments(db: Session):
    return (
        db.query(models.Department)
        .order_by(models.Department.id)
        .all()
    )


def get_department(
    db: Session,
    department_id: int
):
    return (
        db.query(models.Department)
        .filter(models.Department.id == department_id)
        .first()
    )


# ============================================================
# EMPLOYEE CRUD
# ============================================================

def create_employee(
    db: Session,
    employee: schemas.EmployeeCreate
):
    # Check department
    department = (
        db.query(models.Department)
        .filter(models.Department.id == employee.department_id)
        .first()
    )

    if not department:
        raise ValueError("Department not found.")

    # Check duplicate email
    existing_employee = (
        db.query(models.Employee)
        .filter(models.Employee.email == employee.email)
        .first()
    )

    if existing_employee:
        raise ValueError("Employee with this email already exists.")

    new_employee = models.Employee(
        name=employee.name,
        email=employee.email,
        department_id=employee.department_id,
        designation=employee.designation,
        salary=employee.salary,
        joining_date=employee.joining_date
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return new_employee


def get_employees(
    db: Session,
    department_id: int | None = None
):
    query = (
        db.query(models.Employee)
        .filter(models.Employee.is_active == True)
    )

    if department_id is not None:
        query = query.filter(
            models.Employee.department_id == department_id
        )

    return (
        query
        .order_by(models.Employee.id)
        .all()
    )


def get_employee(
    db: Session,
    employee_id: int
):
    return (
        db.query(models.Employee)
        .filter(models.Employee.id == employee_id,
                models.Employee.is_active == True)
        .first()
    )

def get_employee_any_status(
    db: Session,
    employee_id: int
):
    return (
        db.query(models.Employee)
        .filter(
            models.Employee.id == employee_id
        )
        .first()
    )

def update_employee(
    db: Session,
    employee_id: int,
    employee_data: schemas.EmployeeUpdate
):
    employee = get_employee(db, employee_id)

    if not employee:
        return None

    update_data = employee_data.model_dump(
        exclude_unset=True
    )

    # If email is being changed, check duplicate
    if "email" in update_data:
        existing_employee = (
            db.query(models.Employee)
            .filter(
                models.Employee.email == update_data["email"],
                models.Employee.id != employee_id
            )
            .first()
        )

        if existing_employee:
            raise ValueError(
                "Another employee already uses this email."
            )

    # If department is being changed, check department
    if "department_id" in update_data:
        department = (
            db.query(models.Department)
            .filter(
                models.Department.id
                == update_data["department_id"]
            )
            .first()
        )

        if not department:
            raise ValueError("Department not found.")

    for field, value in update_data.items():
        setattr(employee, field, value)

    db.commit()
    db.refresh(employee)

    return employee

def delete_employee(
    db: Session,
    employee_id: int
):
    employee = (
        db.query(models.Employee)
        .filter(
            models.Employee.id == employee_id,
            models.Employee.is_active == True
        )
        .first()
    )

    if not employee:
        return None

    # Soft delete employee
    # Historical payslips remain untouched.
    employee.is_active = False

    db.commit()
    db.refresh(employee)

    return True

# ============================================================
# PAYSLIP CRUD
# ============================================================

def generate_payslip(
    db: Session,
    employee_id: int,
    payslip_data: schemas.PayslipGenerate
):
    # Find employee
    employee = get_employee(db, employee_id)

    if not employee:
        raise ValueError("Employee not found.")

    # Check duplicate payslip
    existing_payslip = (
        db.query(models.Payslip)
        .filter(
            models.Payslip.employee_id == employee_id,
            models.Payslip.month == payslip_data.month,
            models.Payslip.year == payslip_data.year
        )
        .first()
    )

    if existing_payslip:
        raise ValueError(
            "Payslip already exists for this employee "
            "for the selected month and year."
        )

    # Basic salary comes from Employee table
    basic = employee.salary

    # Deductions come from request
    deductions = payslip_data.deductions

    # Calculate net pay
    net_pay = basic - deductions

    # Prevent negative net pay
    if net_pay < 0:
        raise ValueError(
            "Deductions cannot be greater than the basic salary."
        )

    new_payslip = models.Payslip(
        employee_id=employee_id,
        month=payslip_data.month,
        year=payslip_data.year,
        basic=basic,
        deductions=deductions,
        net_pay=net_pay
    )

    db.add(new_payslip)

    try:
        db.commit()
        db.refresh(new_payslip)
    except IntegrityError:
        db.rollback()
        raise ValueError(
            "Payslip already exists for this employee "
            "for the selected month and year."
        )

    return new_payslip


def get_employee_payslips(
    db: Session,
    employee_id: int
):
    return (
        db.query(models.Payslip)
        .filter(models.Payslip.employee_id == employee_id)
        .order_by(
            models.Payslip.year.desc(),
            models.Payslip.month.desc()
        )
        .all()
    )


def get_all_payslips(db: Session):
    return (
        db.query(models.Payslip)
        .order_by(
            models.Payslip.year.desc(),
            models.Payslip.month.desc(),
            models.Payslip.id.desc()
        )
        .all()
    )