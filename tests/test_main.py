import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, Base, engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
test_engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def client():
    # Create test database tables
    Base.metadata.create_all(bind=test_engine)
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Clean up test database
    Base.metadata.drop_all(bind=test_engine)
    if os.path.exists("test.db"):
        os.remove("test.db")

def test_home_page(client):
    """Test that the home page loads correctly"""
    response = client.get("/")
    assert response.status_code == 200
    assert "ProfeAI" in response.text
    assert "Your Personal AI Professor" in response.text

def test_user_registration(client):
    """Test user registration functionality"""
    response = client.post("/register", data={
        "name": "Test User",
        "email": "test@example.com",
        "specialization": "Theory",
        "level": "Beginner"
    })
    
    # Should redirect to dashboard
    assert response.status_code == 303
    assert "/dashboard/" in response.headers["location"]

def test_user_registration_duplicate_email(client):
    """Test handling of duplicate email registration"""
    # Register first user
    client.post("/register", data={
        "name": "User One",
        "email": "test@example.com",
        "specialization": "Theory",
        "level": "Beginner"
    })
    
    # Register second user with same email (should update existing)
    response = client.post("/register", data={
        "name": "User Two",
        "email": "test@example.com",
        "specialization": "Tooling",
        "level": "Advanced"
    })
    
    assert response.status_code == 303

def test_dashboard_requires_valid_user(client):
    """Test that dashboard requires a valid user ID"""
    response = client.get("/dashboard/999")
    assert response.status_code == 404

def test_lesson_generation_flow(client):
    """Test the complete lesson generation flow"""
    # First register a user
    response = client.post("/register", data={
        "name": "Test User",
        "email": "test@example.com",
        "specialization": "Theory",
        "level": "Beginner"
    })
    
    # Extract user ID from redirect
    location = response.headers["location"]
    user_id = location.split("/")[-1]
    
    # Mock the AI service to avoid API calls in tests
    import app.main
    original_generate_lesson = app.main.lesson_generator.generate_lesson
    
    def mock_generate_lesson(*args, **kwargs):
        return {
            "title": "Test Lesson",
            "content": "This is a test lesson content.",
            "exercise": "Complete this test exercise."
        }
    
    app.main.lesson_generator.generate_lesson = mock_generate_lesson
    
    try:
        # Generate a lesson
        response = client.post(f"/generate_lesson/{user_id}")
        assert response.status_code == 303
        assert "/lesson/" in response.headers["location"]
        
        # Extract lesson ID and view the lesson
        lesson_location = response.headers["location"]
        response = client.get(lesson_location)
        assert response.status_code == 200
        assert "Test Lesson" in response.text
        
    finally:
        # Restore original function
        app.main.lesson_generator.generate_lesson = original_generate_lesson

def test_api_endpoints(client):
    """Test API endpoints functionality"""
    # Register a user first
    client.post("/register", data={
        "name": "API Test User",
        "email": "api@example.com",
        "specialization": "Hybrid",
        "level": "Intermediate"
    })
    
    # Test get user API
    response = client.get("/api/user/1")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "API Test User"
    assert data["specialization"] == "Hybrid"
    
    # Test get lessons API (should be empty initially)
    response = client.get("/api/lessons/1")
    assert response.status_code == 200
    lessons = response.json()
    assert isinstance(lessons, list)
    assert len(lessons) == 0

def test_feedback_system(client):
    """Test lesson feedback functionality"""
    # Register user and create a lesson
    response = client.post("/register", data={
        "name": "Feedback User",
        "email": "feedback@example.com", 
        "specialization": "Theory",
        "level": "Beginner"
    })
    
    location = response.headers["location"]
    user_id = location.split("/")[-1]
    
    # Mock lesson generation
    import app.main
    original_generate_lesson = app.main.lesson_generator.generate_lesson
    original_generate_alternative = app.main.lesson_generator.generate_alternative_explanation
    
    app.main.lesson_generator.generate_lesson = lambda *args, **kwargs: {
        "title": "Feedback Test Lesson",
        "content": "Original lesson content"
    }
    
    app.main.lesson_generator.generate_alternative_explanation = lambda *args, **kwargs: "Alternative explanation content"
    
    try:
        # Generate lesson
        response = client.post(f"/generate_lesson/{user_id}")
        lesson_location = response.headers["location"]
        lesson_id = lesson_location.split("/")[-1]
        
        # Submit positive feedback
        response = client.post(f"/feedback/{lesson_id}", data={"feedback_type": "clear"})
        assert response.status_code == 303
        
        # Submit negative feedback (should generate alternative)
        response = client.post(f"/feedback/{lesson_id}", data={"feedback_type": "confused"})
        assert response.status_code == 303
        assert "/lesson/" in response.headers["location"]
        
    finally:
        app.main.lesson_generator.generate_lesson = original_generate_lesson
        app.main.lesson_generator.generate_alternative_explanation = original_generate_alternative