from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import crud
import schemas
from database import get_db


# Create router
router = APIRouter(
    prefix="/payslips",
    tags=["Payroll"]
)


# ============================================================
# GENERATE PAYSLIP
# ============================================================

@router.post(
    "/generate/{employee_id}",
    response_model=schemas.PayslipResponse,
    status_code=status.HTTP_201_CREATED
)
def generate_payslip(
    employee_id: int,
    payslip: schemas.PayslipGenerate,
    db: Session = Depends(get_db)
):
    try:
        return crud.generate_payslip(
            db,
            employee_id,
            payslip
        )

    except ValueError as error:
        message = str(error)

        # Employee does not exist
        if message == "Employee not found.":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=message
            )

        # Duplicate payslip / invalid payroll operation
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )


# ============================================================
# GET PAYSLIPS FOR SPECIFIC EMPLOYEE
# ============================================================

@router.get(
    "/{employee_id}",
    response_model=list[schemas.PayslipResponse],
    status_code=status.HTTP_200_OK
)
def get_employee_payslips(
    employee_id: int,
    db: Session = Depends(get_db)
):
    # First check that employee exists
    employee = crud.get_employee_any_status(
        db,
        employee_id
    )

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found."
        )

    return crud.get_employee_payslips(
        db,
        employee_id
    )


# ============================================================
# GET ALL PAYSLIPS
# ============================================================

@router.get(
    "",
    response_model=list[schemas.PayslipResponse],
    status_code=status.HTTP_200_OK
)
def get_all_payslips(
    db: Session = Depends(get_db)
):
    return crud.get_all_payslips(db)