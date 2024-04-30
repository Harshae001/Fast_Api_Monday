from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["Task_and_Employee_db"]
task_collection = db["Tasks"]
employee_collection = db["Employee"]
total_task_to_each_employee_collection=db["Total tasks for each employee"]
total_tasks_by_status_collection=db["total tasks by status"]


# from mongoimport import MongoDB_connection

def add_tasks():
    try:
        id = int(input("Enter task id: "))
        name = input("Enter task name: ")
        status = input("Enter task status: ")
        task = {"id": id, "name": name, "status": status}
        task_collection.insert_one(task)
        print("Task added successfully.")
    except Exception as e:
        print(f"Error: {e}")

def add_employees():
    try:
        id = int(input("Enter employee id: "))
        name = input("Enter employee name: ")
        employee = {"id": id, "name": name}
        employee_collection.insert_one(employee)
        print("Employee added successfully.")
    except Exception as e:
        print(f"Error: {e}")

def tasks_list():
    try:
        tasks = task_collection.find()
        for task in tasks:
            print(task)
    except Exception as e:
        print(f"Error: {e}")

def employees_list():
    try:
        employees = employee_collection.find()
        for employee in employees:
            print(employee)
    except Exception as e:
        print(f"Error: {e}")

def remove_task():
    try:
        task_to_be_removed = input("Enter task id to be removed: ")
        result = task_collection.delete_one({"id": int(task_to_be_removed)})
        if result.deleted_count > 0:
            print("Task removed successfully.")
        else:
            print("Task not found.")
    except Exception as e:
        print(f"Error: {e}")

def employee_remove():
    try:
        employee_to_be_removed = input("Enter employee id to be removed: ")
        result = employee_collection.delete_one({"id": int(employee_to_be_removed)})
        if result.deleted_count > 0:
            print("Employee removed successfully.")
        else:
            print("Employee not found.")
    except Exception as e:
        print(f"Error: {e}")

def assign_task_to_employee():
    try:
        task_id = int(input("Enter task id: "))
        employee_id = int(input("Enter employee id to assign task to: "))
        task = task_collection.find_one({"id": task_id})
        if task:
            task_collection.update_one({"id": task_id}, {"$push": {"assigned_to": employee_id}})
            print(f"Task {task_id} assigned to employee {employee_id}.")
        else:
            print("Task not found.")
    except Exception as e:
        print(f"Error: {e}")

def deassign_task_from_employee():
    try:
        task_id = int(input("Enter task id to be de-assigned: "))
        task = task_collection.find_one({"id": task_id})
        if task and "assigned_to" in task:
            task_collection.update_one({"id": task_id}, {"$unset": {"assigned_to": ""}})
            print(f"Task {task_id} de-assigned from employee.")
        else:
            print("Task not found or not assigned to any employee.")
    except Exception as e:
        print(f"Error: {e}")


def delete_database():
    try:
        client.drop_database("Task_and_Employee_db")
        print("Database deleted successfully.")
    except Exception as e:
        print(f"Error: {e}")



def main():
    while True:
        print("Select an Option:")
        print("1. Add Task")
        print("2. Add Employee")
        print("3. List Tasks")
        print("4. List Employees")
        print("5. Remove Task")
        print("6. Remove Employee")
        print("7. Assign Task to Employee")
        print("8. Deassign task from employee")
        print("9. Delete database")
        print("10. Exit and close ")
       
        choice = input("Select an option: ")

        if choice == "1":
            add_tasks()
        elif choice == "2":
            add_employees()
        elif choice == "3":
            tasks_list()
        elif choice == "4":
            employees_list()
        elif choice == "5":
            remove_task()
        elif choice == "6":
            employee_remove()
        elif choice == "7":
            assign_task_to_employee()
        elif choice == "8":
            deassign_task_from_employee()
        elif choice == "9":
            delete_database()
        elif choice == "10":
            client.close()
            print("Exiting program and closing connection")
            break    
        else:
            print("Invalid option")

if __name__ == "__main__":
    main()





