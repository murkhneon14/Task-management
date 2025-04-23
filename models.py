from pydantic import BaseModel, Field
from typing import Optional

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    status: str = Field(default="pending", pattern="^(pending|completed)$")

class TaskUpdateStatus(BaseModel):
    status: str = Field(..., pattern="^(pending|completed)$")

class TaskOut(BaseModel):
    id: str
    title: str
    status: str

    class Config:
        orm_mode = True
