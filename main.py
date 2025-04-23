from fastapi import FastAPI, HTTPException, status, Path
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId
from database import task_collection, check_db_connection
from models import TaskCreate, TaskUpdateStatus, TaskOut
import motor.motor_asyncio
from pymongo import ReturnDocument

app = FastAPI(title="Task Management System", description="A basic task management backend using FastAPI and MongoDB.")

@app.on_event("startup")
async def startup_event():
    await check_db_connection()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def task_serializer(task) -> dict:
    return {
        "id": str(task["_id"]),
        "title": task["title"],
        "status": task["status"]
    }

@app.post("/tasks", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate):
    task_dict = task.dict()
    result = await task_collection.insert_one(task_dict)
    new_task = await task_collection.find_one({"_id": result.inserted_id})
    return task_serializer(new_task)

@app.get("/tasks", response_model=list[TaskOut])
async def get_tasks():
    tasks = []
    async for task in task_collection.find():
        tasks.append(task_serializer(task))
    return tasks

@app.patch("/tasks/{task_id}/status", response_model=TaskOut)
async def update_task_status(task_id: str = Path(..., description="The ID of the task to update"), status_update: TaskUpdateStatus = ...):
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid task ID")
    result = await task_collection.find_one_and_update(
        {"_id": ObjectId(task_id)},
        {"$set": {"status": status_update.status}},
        return_document=ReturnDocument.AFTER
    )
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return task_serializer(result)

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str = Path(..., description="The ID of the task to delete")):
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid task ID")
    result = await task_collection.delete_one({"_id": ObjectId(task_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)
