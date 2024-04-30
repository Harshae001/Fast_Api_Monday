from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mongoimport import MongoDB_connection

app = FastAPI()

class Task(BaseModel):
    task_id: int
    name: str
    status: str

class Employee(BaseModel):
    employee_id: int
    name: str

class TaskAssignment(BaseModel):
    task_id: int
    employee_id: int

@app.post("/tasks/")
async def create_task(task: Task):
    try:
        task_obj = task
        MongoDB_connection.task_collection.insert_one(task_obj.dict())
        return {"message": "Task added successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/employees/")
async def create_employee(employee: Employee):
    try:
        employee_obj = employee
        MongoDB_connection.employee_collection.insert_one(employee_obj.dict())
        return {"message": "Employee added successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/assign_task/")
async def assign_task(task_assignment: TaskAssignment):
    try:
        task_id = task_assignment.task_id
        employee_id = task_assignment.employee_id
        task = MongoDB_connection.task_collection.find_one({"id": task_id})
        if task:
            MongoDB_connection.task_collection.update_one(
                {"id": task_id}, {"$set": {"assigned_to": employee_id}}
            )
            return {"message": f"Task {task_id} assigned to employee {employee_id}."}
        else:
            raise HTTPException(status_code=404, detail="Task not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    try:
        result = MongoDB_connection.task_collection.delete_one({"id": task_id})
        if result.deleted_count > 0:
            return {"message": "Task deleted successfully."}
        else:
            raise HTTPException(status_code=404, detail="Task not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/employees/{employee_id}")
async def delete_employee(employee_id: int):
    try:
        result = MongoDB_connection.employee_collection.delete_one({"id": employee_id})
        if result.deleted_count > 0:
            return {"message": "Employee deleted successfully."}
        else:
            raise HTTPException(status_code=404, detail="Employee not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
