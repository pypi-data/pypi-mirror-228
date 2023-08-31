database = {
    "listCompanies": [
        {"__typename": "Company", "id": "company-1",
            "name": "Company A", "industry": "Tech"},
        {"__typename": "Company", "id": "company-2",
            "name": "Company B", "industry": "Finance"},
    ],
    "listDepartments": [
        {"__typename": "Department", "id": "department-1",
            "name": "Engineering", "companyID": "company-1"},
        {"__typename": "Department", "id": "department-2",
            "name": "Marketing", "companyID": "company-1"},
        {"__typename": "Department", "id": "department-3",
            "name": "Finance", "companyID": "company-2"},
    ],
    "listTeams": [
        {"__typename": "Team", "id": "team-1",
            "name": "Backend Team", "departmentID": "department-1"},
        {"__typename": "Team", "id": "team-2",
            "name": "Frontend Team", "departmentID": "department-1"},
        {"__typename": "Team", "id": "team-3",
            "name": "Digital Marketing", "departmentID": "department-2"},
        {"__typename": "Team", "id": "team-4",
            "name": "Accounting", "departmentID": "department-3"},
    ],
    "listEmployees": [
        {"__typename": "Employee", "id": "employee-1", "name": "John Doe",
            "position": "Software Engineer", "teamID": "team-1"},
        {"__typename": "Employee", "id": "employee-2", "name": "Jane Smith",
            "position": "Frontend Developer", "teamID": "team-2"},
        {"__typename": "Employee", "id": "employee-3", "name": "Alex Brown",
            "position": "Marketing Specialist", "teamID": "team-3"},
        {"__typename": "Employee", "id": "employee-4", "name": "Emily Johnson",
            "position": "Accountant", "teamID": "team-4"},
    ],
    "listTasks": [
        {"__typename": "Task", "id": "task-1",
            "description": "Implement new feature", "employeeID": "employee-1"},
        {"__typename": "Task", "id": "task-2",
            "description": "Design homepage layout", "employeeID": "employee-2"},
        {"__typename": "Task", "id": "task-3",
            "description": "Create social media campaign", "employeeID": "employee-3"},
        {"__typename": "Task", "id": "task-4",
            "description": "Prepare monthly financial report", "employeeID": "employee-4"},
    ],
}


new_database = {}
