from fastapi import FastAPI

from database import Base, engine

# Import models so SQLAlchemy knows all tables
import models

# Import API routers
from routers import departments
from routers import employees
from routers import payslips


# ============================================================
# CREATE DATABASE TABLES
# ============================================================

Base.metadata.create_all(bind=engine)


# ============================================================
# CREATE FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Employee & Payroll Management API",
    description=(
        "A complete Employee and Payroll Management System "
        "built using FastAPI, PostgreSQL and SQLAlchemy."
    ),
    version="1.0.0"
)


# ============================================================
# INCLUDE ROUTERS
# ============================================================

app.include_router(departments.router)
app.include_router(employees.router)
app.include_router(payslips.router)


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def home():
    return {
        "message": "Employee & Payroll Management API is running",
        "docs": "/docs"
    }