from pymongo import MongoClient

class MongoDB_connection:
    client = MongoClient("mongodb://localhost:27017")
    db = client["Task_and_Employee_db"]
    task_collection = db["Tasks"]
    employee_collection = db["Employee"]
    total_task_to_each_employee_collection = db["Total tasks for each employee"]
    total_tasks_by_status_collection = db["total tasks by status"]
