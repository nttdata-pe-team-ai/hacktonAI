import pytest
from app.ai_service import LessonGenerator

def test_lesson_generator_initialization():
    """Test that LessonGenerator initializes correctly"""
    generator = LessonGenerator()
    assert generator is not None
    assert hasattr(generator, 'client')

def test_build_system_prompt():
    """Test system prompt generation for different specializations"""
    generator = LessonGenerator()
    
    # Test Theory specialization
    prompt = generator._build_system_prompt("Theory", "Beginner")
    assert "Theory" in prompt or "fundamentals" in prompt
    assert "Beginner" in prompt
    
    # Test Tooling specialization  
    prompt = generator._build_system_prompt("Tooling", "Advanced")
    assert "hands-on" in prompt or "tools" in prompt or "practical" in prompt
    assert "Advanced" in prompt
    
    # Test Hybrid specialization
    prompt = generator._build_system_prompt("Hybrid", "Intermediate")
    assert "theory" in prompt and "practical" in prompt
    assert "Intermediate" in prompt

def test_build_user_prompt():
    """Test user prompt generation"""
    generator = LessonGenerator()
    
    # Test with specific topic
    prompt = generator._build_user_prompt("machine learning", None, "Theory")
    assert "machine learning" in prompt
    
    # Test with feedback
    prompt = generator._build_user_prompt("neural networks", "confused", "Hybrid")
    assert "confused" in prompt
    assert "alternative" in prompt.lower()
    
    # Test without topic (should generate relevant topic)
    prompt = generator._build_user_prompt(None, None, "Tooling")
    assert "lesson" in prompt.lower()

def test_parse_lesson_content():
    """Test lesson content parsing"""
    generator = LessonGenerator()
    
    # Test well-formatted content
    content = """TITLE: Test Lesson Title
CONTENT: This is the main lesson content with explanations and examples.
EXERCISE: Complete this practice exercise."""
    
    parsed = generator._parse_lesson_content(content)
    assert parsed["title"] == "Test Lesson Title"
    assert "main lesson content" in parsed["content"]
    assert parsed["exercise"] == "Complete this practice exercise."
    
    # Test content without clear structure
    simple_content = "This is just plain lesson content without structure."
    parsed = generator._parse_lesson_content(simple_content)
    assert parsed["content"] == simple_content
    assert parsed["title"] == "AI Lesson"  # Default title

def test_generate_fallback_lesson():
    """Test fallback lesson generation"""
    generator = LessonGenerator()
    
    # Test Theory fallback
    lesson = generator._generate_fallback_lesson("Theory", "Beginner")
    assert "title" in lesson
    assert "content" in lesson
    assert "Machine Learning" in lesson["title"] or "AI" in lesson["content"]
    
    # Test Tooling fallback
    lesson = generator._generate_fallback_lesson("Tooling", "Advanced")
    assert "OpenAI" in lesson["title"] or "API" in lesson["content"]
    
    # Test unknown specialization (should default to Theory)
    lesson = generator._generate_fallback_lesson("Unknown", "Beginner")
    assert lesson is not None
    assert "title" in lesson and "content" in lesson