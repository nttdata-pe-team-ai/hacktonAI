# ProfeAI - Your AI Professor with Emotional Intelligence

🤖 **ProfeAI** is an MIT-style AI professor that adapts to your learning style, detects confusion or frustration, and provides personalized AI education in theory, tooling, or both.

## ✨ Features

- **Personalized Learning**: Choose your focus - AI Theory, Practical Tooling, or Hybrid approach
- **Emotional Intelligence**: ProfeAI detects when you're confused or frustrated and adapts explanations
- **Adaptive Content**: Generated lessons using GPT-4o based on your level and feedback
- **Progress Tracking**: Monitor your learning journey with completion stats
- **Interactive Feedback**: Simple buttons to provide feedback and get alternative explanations
- **Hands-on Examples**: Code examples and practical exercises for tooling-focused learning

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Clone the repository
git clone https://github.com/nttdata-pe-team-ai/hacktonAI.git
cd hacktonAI

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your OpenAI API key
```

### 2. Configure OpenAI API

Add your OpenAI API key to the `.env` file:

```
OPENAI_API_KEY=your_openai_api_key_here
SECRET_KEY=your_secret_key_for_sessions
DEBUG=True
```

### 3. Run the Application

```bash
# Start the server
python main.py
```

Visit http://localhost:8000 in your browser to start learning!

## 🎯 How It Works

1. **Register**: Enter your name, email, and choose your learning specialization
2. **Learn**: Generate personalized lessons based on your preferences
3. **Feedback**: Use the emotional feedback buttons if you're confused or frustrated
4. **Adapt**: ProfeAI generates alternative explanations when you need them
5. **Progress**: Track your completed lessons and overall progress

## 🧠 Learning Specializations

### Theory Focus
- AI fundamentals and mathematical foundations
- Algorithm explanations with real-world analogies
- Conceptual understanding of ML, deep learning, and AI systems

### Tooling Focus  
- Hands-on AI development tools and frameworks
- Code examples and practical implementations
- Integration guides and deployment strategies

### Hybrid Approach
- Perfect blend of theory and practice
- Connect mathematical concepts to code implementations
- Build understanding through both explanation and application

## 🏗️ Architecture

```
hacktonAI/
├── app/
│   ├── main.py          # FastAPI application
│   ├── database.py      # SQLAlchemy models and database setup
│   ├── schemas.py       # Pydantic schemas
│   └── ai_service.py    # OpenAI integration and lesson generation
├── templates/           # Jinja2 HTML templates
├── static/
│   ├── css/            # Styles
│   └── js/             # Frontend JavaScript
├── main.py             # Application entry point
├── requirements.txt    # Python dependencies
└── .env.example       # Environment configuration template
```

## 🔧 Technology Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Database**: SQLite (easily configurable to PostgreSQL)
- **AI**: OpenAI GPT-4o API
- **Styling**: Modern CSS with CSS Grid and Flexbox
- **Deployment**: GitHub Codespaces ready

## 📚 API Endpoints

- `GET /` - Home page and user registration
- `POST /register` - Create or update user profile
- `GET /dashboard/{user_id}` - User dashboard with progress
- `POST /generate_lesson/{user_id}` - Generate new lesson
- `GET /lesson/{lesson_id}` - View specific lesson
- `POST /feedback/{lesson_id}` - Submit lesson feedback
- `POST /complete_lesson/{lesson_id}` - Mark lesson as completed

## 🧪 Testing

Basic tests are located in the `tests/` directory. Run them with:

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest tests/
```

## 🚀 Deployment

### GitHub Codespaces

This project is pre-configured for GitHub Codespaces:

1. Click "Code" → "Open with Codespaces" in the GitHub repository
2. Wait for the environment to set up
3. Add your OpenAI API key to `.env`
4. Run `python main.py`

### Local Development

```bash
# Development server with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Deployment

For production deployment, consider:
- Using PostgreSQL instead of SQLite
- Setting up proper environment variables
- Using a reverse proxy like Nginx
- Implementing proper logging and monitoring

## 🎨 Customization

### Adding New Learning Specializations

1. Update the specialization options in `templates/index.html`
2. Modify the AI service prompts in `app/ai_service.py`
3. Add specialization-specific logic in lesson generation

### Extending Emotional Intelligence

The current implementation uses simple feedback buttons. To integrate with Hume AI or other emotion detection APIs:

1. Add the emotion detection service to `app/ai_service.py`
2. Update the feedback collection in templates
3. Modify the lesson adaptation logic

### Custom AI Models

To use different AI models or providers:
1. Update the model configuration in `app/ai_service.py`
2. Modify the prompt engineering for different model capabilities
3. Test lesson quality with the new model

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

If you encounter issues:

1. Check that your OpenAI API key is valid and has credits
2. Ensure all dependencies are installed correctly
3. Check the console logs for error messages
4. Open an issue in the GitHub repository

---

Built with ❤️ for the AI learning community. Happy learning with ProfeAI! 🚀
