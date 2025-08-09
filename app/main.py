from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import desc
import os
from dotenv import load_dotenv
from typing import List, Optional
import json

from app.database import get_db, create_tables, User, Lesson, Feedback, Progress
from app.schemas import UserCreate, UserResponse, LessonResponse, FeedbackCreate
from app.ai_service import LessonGenerator
from datetime import datetime

# Load environment variables
load_dotenv()

app = FastAPI(title="ProfeAI", description="AI Professor with Emotional Intelligence")

# Create database tables
create_tables()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize AI service
lesson_generator = LessonGenerator()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page - user registration/login"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/register")
async def register_user(
    name: str = Form(...),
    email: str = Form(...),
    specialization: str = Form(...),
    level: str = Form(default="Beginner"),
    db: Session = Depends(get_db)
):
    """Register a new user"""
    # Check if user exists
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        # Update existing user's preferences
        existing_user.name = name
        existing_user.specialization = specialization
        existing_user.level = level
        db.commit()
        user_id = existing_user.id
    else:
        # Create new user
        user = User(
            name=name,
            email=email,
            specialization=specialization,
            level=level
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        user_id = user.id
    
    # Redirect to dashboard
    response = RedirectResponse(url=f"/dashboard/{user_id}", status_code=303)
    return response

@app.get("/dashboard/{user_id}", response_class=HTMLResponse)
async def dashboard(request: Request, user_id: int, db: Session = Depends(get_db)):
    """User dashboard"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get recent lessons
    recent_lessons = db.query(Lesson).filter(
        Lesson.user_id == user_id
    ).order_by(desc(Lesson.created_at)).limit(5).all()
    
    # Calculate progress
    total_lessons = db.query(Lesson).filter(Lesson.user_id == user_id).count()
    completed_lessons = db.query(Lesson).filter(
        Lesson.user_id == user_id, Lesson.completed == True
    ).count()
    
    progress_percentage = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user,
        "recent_lessons": recent_lessons,
        "total_lessons": total_lessons,
        "completed_lessons": completed_lessons,
        "progress_percentage": round(progress_percentage, 1)
    })

@app.post("/generate_lesson/{user_id}")
async def generate_lesson(
    user_id: int,
    topic: str = Form(default=""),
    db: Session = Depends(get_db)
):
    """Generate a new lesson for the user"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Generate lesson using AI service
    lesson_data = lesson_generator.generate_lesson(
        specialization=user.specialization,
        level=user.level,
        topic=topic if topic else None
    )
    
    # Save lesson to database
    lesson = Lesson(
        user_id=user_id,
        title=lesson_data["title"],
        content=lesson_data["content"],
        lesson_type=user.specialization,
        difficulty=user.level
    )
    
    # Add exercise if present
    if lesson_data.get("exercise"):
        lesson.content += f"\n\n**Practice Exercise:**\n{lesson_data['exercise']}"
    
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    
    # Update user's total lesson count
    user.total_lessons += 1
    db.commit()
    
    # Redirect to lesson view
    response = RedirectResponse(url=f"/lesson/{lesson.id}", status_code=303)
    return response

@app.get("/lesson/{lesson_id}", response_class=HTMLResponse)
async def view_lesson(request: Request, lesson_id: int, db: Session = Depends(get_db)):
    """View a specific lesson"""
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    user = db.query(User).filter(User.id == lesson.user_id).first()
    
    return templates.TemplateResponse("lesson.html", {
        "request": request,
        "lesson": lesson,
        "user": user
    })

@app.post("/feedback/{lesson_id}")
async def submit_feedback(
    lesson_id: int,
    feedback_type: str = Form(...),
    db: Session = Depends(get_db)
):
    """Submit feedback for a lesson"""
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    # Save feedback
    feedback = Feedback(
        user_id=lesson.user_id,
        lesson_id=lesson_id,
        feedback_type=feedback_type
    )
    db.add(feedback)
    db.commit()
    
    # If feedback is negative (confused/frustrated), generate alternative explanation
    if feedback_type in ["confused", "frustrated"]:
        try:
            alternative_content = lesson_generator.generate_alternative_explanation(
                lesson.content, feedback_type
            )
            
            # Create a new lesson with the alternative explanation
            new_lesson = Lesson(
                user_id=lesson.user_id,
                title=f"Alternative: {lesson.title}",
                content=alternative_content,
                lesson_type=lesson.lesson_type,
                difficulty=lesson.difficulty
            )
            db.add(new_lesson)
            db.commit()
            db.refresh(new_lesson)
            
            return RedirectResponse(url=f"/lesson/{new_lesson.id}?message=alternative", status_code=303)
        except Exception as e:
            # If AI service fails, just acknowledge the feedback
            return RedirectResponse(url=f"/lesson/{lesson_id}?message=feedback_received", status_code=303)
    
    # For positive feedback, mark lesson as helpful
    return RedirectResponse(url=f"/lesson/{lesson_id}?message=thanks", status_code=303)

@app.post("/complete_lesson/{lesson_id}")
async def complete_lesson(lesson_id: int, db: Session = Depends(get_db)):
    """Mark a lesson as completed"""
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    if not lesson.completed:
        lesson.completed = True
        lesson.completion_time = datetime.utcnow()
        
        # Update user's completed lesson count
        user = db.query(User).filter(User.id == lesson.user_id).first()
        user.completed_lessons += 1
        
        db.commit()
    
    return RedirectResponse(url=f"/dashboard/{lesson.user_id}?message=lesson_completed", status_code=303)

@app.get("/api/user/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user information via API"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/api/lessons/{user_id}", response_model=List[LessonResponse])
async def get_user_lessons(user_id: int, db: Session = Depends(get_db)):
    """Get all lessons for a user via API"""
    lessons = db.query(Lesson).filter(Lesson.user_id == user_id).order_by(desc(Lesson.created_at)).all()
    return lessons

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)