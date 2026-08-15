# Employee & Payroll Management System

A full-stack Employee & Payroll Management System built using FastAPI, PostgreSQL, SQLAlchemy, and Streamlit.

This project manages departments, employees, and employee payroll records. It provides REST APIs through FastAPI and a user-friendly Streamlit frontend.

---

## 📌 Project Overview

The Employee & Payroll Management System is designed to provide a centralized system for managing employee information and payroll records.

The system allows HR users to:

- Create and view departments
- Add, update, view and delete employees
- Store employee salary and joining date
- Generate payslips for employees
- Calculate net pay using:

  Net Pay = Basic Salary - Deductions

- View payslips for a specific employee
- View complete payroll history
- Prevent duplicate payslips for the same employee, month and year

Historical payroll records are maintained even when an employee is deleted.

---

## 🚀 Features

### Department Management

- Create departments
- View all departments
- View department details
- Store manager information

### Employee Management

- Add new employees
- View all employees
- View employee details
- Update employee information
- Delete employees

### Payroll Management

- Generate employee payslips
- Store basic salary
- Store deductions
- Calculate net pay
- View employee payroll history
- View complete payroll history
- Prevent duplicate payslips

### Frontend

The project includes a Streamlit frontend for interacting with the backend.

---

## 🛠️ Technologies Used

### Backend
- Python
- FastAPI
- Uvicorn
- Pydantic

### Database
- PostgreSQL
- SQLAlchemy

### Frontend
- Streamlit

### Development Tools
- Visual Studio Code
- pgAdmin
- Swagger UI

---

## 📂 Project Structure

```text
Employee_Payroll_Project/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   │
│   └── routers/
│       ├── __init__.py
│       ├── departments.py
│       ├── employees.py
│       └── payslips.py
│
├── frontend/
│   └── app.py
│
├── .env
├── README.md
├── requirements.txt
└── venv/