from datetime import date
from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ============================================================
# DEPARTMENT SCHEMAS
# ============================================================

class DepartmentBase(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    manager_name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentResponse(DepartmentBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# ============================================================
# EMPLOYEE SCHEMAS
# ============================================================

class EmployeeBase(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    email: EmailStr

    department_id: int = Field(
        ...,
        gt=0
    )

    designation: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    salary: float = Field(
        ...,
        gt=0
    )

    joining_date: date


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    email: EmailStr | None = None

    department_id: int | None = Field(
        default=None,
        gt=0
    )

    designation: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    salary: float | None = Field(
        default=None,
        gt=0
    )

    joining_date: date | None = None


class EmployeeResponse(EmployeeBase):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


# ============================================================
# PAYSLIP SCHEMAS
# ============================================================

class PayslipGenerate(BaseModel):
    month: int = Field(
        ...,
        ge=1,
        le=12
    )

    year: int = Field(
        ...,
        ge=2000,
        le=2100
    )

    deductions: float = Field(
        default=0,
        ge=0
    )


class PayslipResponse(BaseModel):
    id: int
    employee_id: int
    month: int
    year: int
    basic: float
    deductions: float
    net_pay: float

    model_config = ConfigDict(from_attributes=True)