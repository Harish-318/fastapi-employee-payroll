from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

import crud
import schemas
from database import get_db


# Create router
router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)


# ============================================================
# GET ALL EMPLOYEES
# ============================================================

@router.get(
    "",
    response_model=list[schemas.EmployeeResponse],
    status_code=status.HTTP_200_OK
)
def get_employees(
    department_id: int | None = Query(
        default=None,
        gt=0,
        description="Optional department ID filter"
    ),
    db: Session = Depends(get_db)
):
    return crud.get_employees(
        db,
        department_id=department_id
    )


# ============================================================
# GET EMPLOYEE BY ID
# ============================================================

@router.get(
    "/{employee_id}",
    response_model=schemas.EmployeeResponse,
    status_code=status.HTTP_200_OK
)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    employee = crud.get_employee(
        db,
        employee_id
    )

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found."
        )

    return employee


# ============================================================
# CREATE EMPLOYEE
# ============================================================

@router.post(
    "",
    response_model=schemas.EmployeeResponse,
    status_code=status.HTTP_201_CREATED
)
def create_employee(
    employee: schemas.EmployeeCreate,
    db: Session = Depends(get_db)
):
    try:
        return crud.create_employee(
            db,
            employee
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


# ============================================================
# UPDATE EMPLOYEE
# ============================================================

@router.put(
    "/{employee_id}",
    response_model=schemas.EmployeeResponse,
    status_code=status.HTTP_200_OK
)
def update_employee(
    employee_id: int,
    employee: schemas.EmployeeUpdate,
    db: Session = Depends(get_db)
):
    try:
        updated_employee = crud.update_employee(
            db,
            employee_id,
            employee
        )

        if not updated_employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found."
            )

        return updated_employee

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


# ============================================================
# DELETE EMPLOYEE
# ============================================================

@router.delete(
    "/{employee_id}",
    status_code=status.HTTP_200_OK
)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    try:
        result = crud.delete_employee(
            db,
            employee_id
        )

        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found."
            )

        return {
            "message": "Employee deleted successfully."
        }

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )