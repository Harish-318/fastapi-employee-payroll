import streamlit as st
import requests


# ============================================================
# CONFIG
# ============================================================

st.set_page_config(
    page_title="Employee Payroll Management",
    page_icon="💼",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000"


# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #667eea, #764ba2);
}

[data-testid="stSidebar"] {
    background: #202a3e;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

.card {
    padding: 20px;
    border-radius: 15px;
    background: rgba(255,255,255,0.14);
    border: 1px solid rgba(255,255,255,0.25);
    margin-bottom: 15px;
}

.main-title {
    font-size: 36px;
    font-weight: 700;
    color: white;
}

.sub-title {
    color: rgba(255,255,255,0.85);
    font-size: 17px;
}

[data-testid="stMetric"] {
    background: rgba(255,255,255,0.14);
    border-radius: 15px;
    padding: 15px;
    border: 1px solid rgba(255,255,255,0.25);
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# API FUNCTION
# ============================================================

def api(method, endpoint, **kwargs):

    try:
        return requests.request(
            method,
            API_URL + endpoint,
            timeout=10,
            **kwargs
        )

    except requests.exceptions.ConnectionError:
        st.error("❌ FastAPI server is not running.")
        return None

    except requests.exceptions.Timeout:
        st.error("❌ API request timed out.")
        return None

    except requests.exceptions.RequestException as e:
        st.error(f"❌ API Error: {e}")
        return None


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("💼 Employee Payroll")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "🏢 Departments",
        "👨‍💼 Employees",
        "💰 Payroll"
    ]
)

st.sidebar.markdown("---")

# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.markdown(
        '<div class="main-title">'
        '💼 Employee & Payroll Management'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">'
        'Manage departments, employees and payroll from one place.'
        '</div>',
        unsafe_allow_html=True
    )

    d = api("GET", "/departments")
    e = api("GET", "/employees")
    p = api("GET", "/payslips")

    departments = d.json() if d and d.status_code == 200 else []
    employees = e.json() if e and e.status_code == 200 else []
    payslips = p.json() if p and p.status_code == 200 else []

    c1, c2, c3 = st.columns(3)

    c1.metric("🏢 Departments", len(departments))
    c2.metric("👨‍💼 Employees", len(employees))
    c3.metric("💰 Payslips", len(payslips))

    st.markdown("---")

    st.subheader("📊 System Overview")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
        <div class="card">

        ### 🏢 Departments

        Manage departments and managers.

        • Add department  
        • View departments  
        • View department details

        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="card">

        ### 👨‍💼 Employees

        Manage employee information.

        • Add employee  
        • View employees  
        • Update employee  
        • Delete employee

        </div>
        """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
        <div class="card">

        ### 💰 Payroll

        Manage employee payslips.

        • Generate payslip  
        • View employee history  
        • View complete payroll

        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="card">

        ### 🔗 Technology

        **Frontend:** Streamlit  
        **Backend:** FastAPI  
        **ORM:** SQLAlchemy  
        **Database:** PostgreSQL

        </div>
        """, unsafe_allow_html=True)


# ============================================================
# DEPARTMENTS
# ============================================================

elif page == "🏢 Departments":

    st.title("🏢 Departments")

    tab1, tab2, tab3 = st.tabs([
        "➕ Add",
        "📋 View All",
        "🔍 Details"
    ])

    # --------------------------------------------------------
    # ADD DEPARTMENT
    # --------------------------------------------------------

    with tab1:

        with st.form("department_form"):

            name = st.text_input(
                "Department Name"
            )

            manager = st.text_input(
                "Manager Name"
            )

            submit = st.form_submit_button(
                "Add Department"
            )

            if submit:

                if not name.strip() or not manager.strip():

                    st.error(
                        "Department name and manager are required."
                    )

                else:

                    response = api(
                        "POST",
                        "/departments",
                        json={
                            "name": name.strip(),
                            "manager_name": manager.strip()
                        }
                    )

                    if response and response.status_code in [200, 201]:

                        st.success(
                            "✅ Department added successfully!"
                        )

                        st.rerun()

                    elif response:

                        try:
                            detail = response.json().get(
                                "detail",
                                response.text
                            )
                        except:
                            detail = response.text

                        st.error(
                            f"❌ {detail}"
                        )

    # --------------------------------------------------------
    # VIEW DEPARTMENTS
    # --------------------------------------------------------

    with tab2:

        response = api(
            "GET",
            "/departments"
        )

        if response and response.status_code == 200:

            data = response.json()

            if data:

                st.dataframe(
                    data,
                    use_container_width=True,
                    hide_index=True
                )

            else:
                st.info("No departments found.")

    # --------------------------------------------------------
    # DEPARTMENT DETAILS
    # --------------------------------------------------------

    with tab3:

        department_id = st.number_input(
            "Department ID",
            min_value=1,
            step=1
        )

        if st.button("View Department"):

            response = api(
                "GET",
                f"/departments/{department_id}"
            )

            if response and response.status_code == 200:

                st.json(response.json())

            elif response and response.status_code == 404:

                st.error("❌ Department not found.")

            elif response:

                st.error(
                    f"❌ Error {response.status_code}"
                )


# ============================================================
# EMPLOYEES
# ============================================================

elif page == "👨‍💼 Employees":

    st.title("👨‍💼 Employees")

    # Load departments

    d = api(
        "GET",
        "/departments"
    )

    departments = (
        d.json()
        if d and d.status_code == 200
        else []
    )

    department_map = {
        x["name"]: x["id"]
        for x in departments
    }

    tab1, tab2, tab3, tab4 = st.tabs([
        "➕ Add",
        "📋 Employees",
        "✏️ Update",
        "🗑️ Delete"
    ])

    # --------------------------------------------------------
    # ADD EMPLOYEE
    # --------------------------------------------------------

    with tab1:

        if not department_map:

            st.warning(
                "Create a department first."
            )

        else:

            with st.form("employee_form"):

                name = st.text_input("Employee Name")

                email = st.text_input("Email")

                department = st.selectbox(
                    "Department",
                    list(department_map.keys())
                )

                designation = st.text_input(
                    "Designation"
                )

                salary = st.number_input(
                    "Salary",
                    min_value=0.0,
                    step=1000.0
                )

                joining_date = st.date_input(
                    "Joining Date"
                )

                submit = st.form_submit_button(
                    "Add Employee"
                )

                if submit:

                    if (
                        not name.strip()
                        or not email.strip()
                        or not designation.strip()
                    ):

                        st.error(
                            "Please fill all required fields."
                        )

                    elif salary <= 0:

                        st.error(
                            "Salary must be greater than 0."
                        )

                    else:

                        response = api(
                            "POST",
                            "/employees",
                            json={
                                "name": name.strip(),
                                "email": email.strip(),
                                "department_id":
                                    department_map[department],
                                "designation":
                                    designation.strip(),
                                "salary": salary,
                                "joining_date":
                                    str(joining_date)
                            }
                        )

                        if response and response.status_code in [200, 201]:

                            st.success(
                                "✅ Employee added successfully!"
                            )

                            st.rerun()

                        elif response:

                            try:
                                detail = response.json().get(
                                    "detail",
                                    response.text
                                )
                            except:
                                detail = response.text

                            st.error(
                                f"❌ {detail}"
                            )

    # --------------------------------------------------------
    # VIEW EMPLOYEES
    # --------------------------------------------------------

    with tab2:

        response = api(
            "GET",
            "/employees"
        )

        if response and response.status_code == 200:

            employees = response.json()

            if employees:

                st.dataframe(
                    employees,
                    use_container_width=True,
                    hide_index=True
                )

                st.markdown("---")

                employee_id = st.number_input(
                    "Employee ID for details",
                    min_value=1,
                    step=1
                )

                if st.button("View Employee"):

                    r = api(
                        "GET",
                        f"/employees/{employee_id}"
                    )

                    if r and r.status_code == 200:
                        st.json(r.json())

                    elif r and r.status_code == 404:
                        st.error(
                            "❌ Employee not found."
                        )

            else:

                st.info("No active employees found.")

    # --------------------------------------------------------
    # UPDATE EMPLOYEE
    # --------------------------------------------------------

    with tab3:

        employee_id = st.number_input(
            "Employee ID",
            min_value=1,
            step=1,
            key="update_id"
        )

        designation = st.text_input(
            "New Designation"
        )

        salary = st.number_input(
            "New Salary",
            min_value=0.0,
            step=1000.0,
            key="update_salary"
        )

        if st.button("Update Employee"):

            data = {}

            if designation.strip():
                data["designation"] = designation.strip()

            if salary > 0:
                data["salary"] = salary

            if not data:

                st.warning(
                    "Enter at least one value."
                )

            else:

                response = api(
                    "PUT",
                    f"/employees/{employee_id}",
                    json=data
                )

                if response and response.status_code == 200:

                    st.success(
                        "✅ Employee updated successfully!"
                    )

                    st.rerun()

                elif response and response.status_code == 404:

                    st.error(
                        "❌ Employee not found."
                    )

                elif response:

                    st.error(
                        f"❌ Error {response.status_code}: "
                        f"{response.text}"
                    )

    # --------------------------------------------------------
    # DELETE EMPLOYEE
    # --------------------------------------------------------

    with tab4:

        employee_id = st.number_input(
            "Employee ID",
            min_value=1,
            step=1,
            key="delete_id"
        )

        st.warning(
            "Delete performs a soft delete. "
            "Historical payslips remain محفوظ."
        )

        if st.button("Delete Employee"):

            response = api(
                "DELETE",
                f"/employees/{employee_id}"
            )

            if response and response.status_code == 200:

                st.success(
                    "✅ Employee deleted successfully!"
                )

                st.rerun()

            elif response and response.status_code == 404:

                st.error(
                    "❌ Employee not found."
                )

            elif response:

                st.error(
                    f"❌ Error {response.status_code}: "
                    f"{response.text}"
                )


# ============================================================
# PAYROLL
# ============================================================

elif page == "💰 Payroll":

    st.title("💰 Payroll")

    # Load active employees

    response = api(
        "GET",
        "/employees"
    )

    employees = (
        response.json()
        if response and response.status_code == 200
        else []
    )

    tab1, tab2, tab3 = st.tabs([
        "➕ Generate",
        "📋 Employee History",
        "📊 All Payroll"
    ])

    with tab3:

     st.subheader("📊 All Payroll")

    response = api("GET", "/payslips")

    if response and response.status_code == 200:

        data = response.json()

        if data:

            st.dataframe(
                data,
                use_container_width=True,
                hide_index=True
            )

        else:
            st.info("No payroll records found.")

    elif response:
        st.error(f"❌ Error {response.status_code}")

    else:
        st.error("❌ Backend is not responding.")

    # --------------------------------------------------------
    # GENERATE PAYSLIP
    # --------------------------------------------------------

    with tab1:

        if not employees:

            st.warning(
                "No active employees available."
            )

        else:

            employee_map = {
                f"{e['id']} - {e['name']}": e
                for e in employees
            }

            selected = st.selectbox(
                "Employee",
                list(employee_map.keys())
            )

            employee = employee_map[selected]

            st.info(
                f"Basic Salary: "
                f"₹{employee['salary']:,.2f}"
            )

            c1, c2 = st.columns(2)

            with c1:

                month = st.selectbox(
                    "Month",
                    range(1, 13),
                    index=7
                )

            with c2:

                year = st.number_input(
                    "Year",
                    min_value=2020,
                    max_value=2100,
                    value=2026
                )

            deductions = st.number_input(
                "Deductions",
                min_value=0.0,
                max_value=float(employee["salary"]),
                step=500.0
            )

            net_pay = (
                float(employee["salary"])
                - float(deductions)
            )

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Basic",
                f"₹{employee['salary']:,.2f}"
            )

            c2.metric(
                "Deductions",
                f"₹{deductions:,.2f}"
            )

            c3.metric(
                "Net Pay",
                f"₹{net_pay:,.2f}"
            )

            if st.button(
                "💰 Generate Payslip"
            ):

                response = api(
                    "POST",
                    f"/payslips/generate/{employee['id']}",
                    json={
                        "month": month,
                        "year": int(year),
                        "deductions": deductions
                    }
                )

                if response and response.status_code in [200, 201]:

                    st.success(
                        "✅ Payslip generated successfully!"
                    )

                    st.json(response.json())

                elif response:

                    try:
                        detail = response.json().get(
                            "detail",
                            response.text
                        )
                    except:
                        detail = response.text

                    st.error(
                        f"❌ {detail}"
                    )

    # --------------------------------------------------------
    # EMPLOYEE HISTORY
    # --------------------------------------------------------

    with tab2:

        employee_id = st.number_input(
            "Employee ID",
            min_value=1,
            step=1,
            key="payroll_employee_id"
        )

        if st.button(
            "View Payslips"
        ):

            response = api(
                "GET",
                f"/payslips/{employee_id}"
            )

            if response and response.status_code == 200:

                data = response.json()

                if data:

                    st.dataframe(
                        data,
                        use_container_width=True,
                        hide_index=True
                    )

                else:

                    st.info(
                        "No payslips found."
                    )

            elif response and response.status_code == 404:

                st.error(
                    "❌ Employee not found."
                )

            elif response:

                st.error(
                    f"❌ Error {response.status_code}"
                )

