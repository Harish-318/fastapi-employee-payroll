from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    Boolean,
    ForeignKey,
    UniqueConstraint
)
from sqlalchemy.orm import relationship

from database import Base


# ============================================================
# DEPARTMENT TABLE
# ============================================================

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    manager_name = Column(String(100), nullable=False)

    # One Department -> Many Employees
    employees = relationship(
        "Employee",
        back_populates="department"
    )


# ============================================================
# EMPLOYEE TABLE
# ============================================================

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True, index=True)

    department_id = Column(
        Integer,
        ForeignKey("departments.id"),
        nullable=False
    )

    designation = Column(String(100), nullable=False)
    salary = Column(Float, nullable=False)
    joining_date = Column(Date, nullable=False)

    is_active = Column(Boolean, nullable=False, default=True)

    department = relationship(
        "Department",
        back_populates="employees"
    )

    payslips = relationship(
        "Payslip",
        back_populates="employee"
    )

# ============================================================
# PAYSLIP TABLE
# ============================================================

class Payslip(Base):
    __tablename__ = "payslips"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(
        Integer,
        ForeignKey("employees.id"),
        nullable=False
    )

    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)

    basic = Column(Float, nullable=False)
    deductions = Column(Float, nullable=False)
    net_pay = Column(Float, nullable=False)

    # Employee -> Payslips
    employee = relationship(
        "Employee",
        back_populates="payslips"
    )

    # Prevent duplicate payslip for the same employee/month/year
    __table_args__ = (
        UniqueConstraint(
            "employee_id",
            "month",
            "year",
            name="unique_employee_month_year"
        ),
    )