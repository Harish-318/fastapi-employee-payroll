from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import crud
import schemas
from database import get_db


# Create router
router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)


# ============================================================
# GET ALL DEPARTMENTS
# ============================================================

@router.get(
    "",
    response_model=list[schemas.DepartmentResponse],
    status_code=status.HTTP_200_OK
)
def get_departments(
    db: Session = Depends(get_db)
):
    return crud.get_departments(db)


# ============================================================
# GET DEPARTMENT BY ID
# ============================================================

@router.get(
    "/{department_id}",
    response_model=schemas.DepartmentResponse,
    status_code=status.HTTP_200_OK
)
def get_department(
    department_id: int,
    db: Session = Depends(get_db)
):
    department = crud.get_department(
        db,
        department_id
    )

    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found."
        )

    return department


# ============================================================
# CREATE DEPARTMENT
# ============================================================

@router.post(
    "",
    response_model=schemas.DepartmentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_department(
    department: schemas.DepartmentCreate,
    db: Session = Depends(get_db)
):
    try:
        return crud.create_department(
            db,
            department
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )