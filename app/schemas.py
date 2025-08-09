from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    specialization: str
    level: Optional[str] = "Beginner"

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    specialization: str
    level: str
    total_lessons: int
    completed_lessons: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class LessonCreate(BaseModel):
    title: str
    content: str
    lesson_type: str
    difficulty: str

class LessonResponse(BaseModel):
    id: int
    title: str
    content: str
    lesson_type: str
    difficulty: str
    completed: bool
    created_at: datetime
    completion_time: Optional[datetime]
    
    class Config:
        from_attributes = True

class FeedbackCreate(BaseModel):
    lesson_id: int
    feedback_type: str

class FeedbackResponse(BaseModel):
    id: int
    lesson_id: int
    feedback_type: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class ProgressResponse(BaseModel):
    topic: str
    progress_percentage: float
    last_updated: datetime
    
    class Config:
        from_attributes = True