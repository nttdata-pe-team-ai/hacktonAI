import openai
import os
from typing import Dict, List
import json

class LessonGenerator:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key and api_key.strip() and api_key != "your_openai_api_key_here":
            self.client = openai.OpenAI(api_key=api_key)
            self.has_api_key = True
        else:
            self.client = None
            self.has_api_key = False
            print("⚠️ OpenAI API key not found. Using fallback lessons only.")
        
    def generate_lesson(self, specialization: str, level: str, topic: str = None, user_feedback: str = None) -> Dict[str, str]:
        """Generate a personalized lesson based on user parameters"""
        
        # If no API key available, use fallback immediately
        if not self.has_api_key:
            return self._generate_fallback_lesson(specialization, level, topic)
        
        # Build the prompt based on specialization and level
        system_prompt = self._build_system_prompt(specialization, level)
        user_prompt = self._build_user_prompt(topic, user_feedback, specialization)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Using gpt-4o-mini for cost efficiency in demo
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            return self._parse_lesson_content(content)
            
        except Exception as e:
            return self._generate_fallback_lesson(specialization, level, topic)
    
    def _build_system_prompt(self, specialization: str, level: str) -> str:
        """Build system prompt based on user's specialization and level"""
        base_prompt = """You are ProfeAI, an MIT-style AI professor with emotional intelligence. 
        You excel at teaching both AI theory and practical tooling with clarity and adaptability.
        
        Your teaching style:
        - Clear, concise explanations with concrete examples
        - Use analogies when helpful
        - Break complex concepts into digestible parts
        - Provide practical applications
        - Encourage experimentation and hands-on learning
        
        """
        
        if specialization == "Theory":
            base_prompt += """Focus on AI fundamentals, algorithms, ML concepts, and mathematical foundations.
            Use rigorous but accessible explanations with real-world analogies."""
        elif specialization == "Tooling":
            base_prompt += """Focus on hands-on AI development tools, coding practices, integrations, 
            and practical implementation. Include code examples and step-by-step guides."""
        else:  # Hybrid
            base_prompt += """Combine theoretical understanding with practical application. 
            Explain the 'why' behind concepts and immediately show 'how' to implement them."""
        
        base_prompt += f"\n\nUser level: {level}. Adjust complexity accordingly."
        
        return base_prompt
    
    def _build_user_prompt(self, topic: str, user_feedback: str, specialization: str) -> str:
        """Build user prompt for lesson generation"""
        if user_feedback:
            prompt = f"The user was {user_feedback} with the previous explanation. Please provide an alternative explanation "
            if topic:
                prompt += f"for the topic: {topic}"
            prompt += ". Use different analogies or examples to make it clearer."
        elif topic:
            prompt = f"Generate a lesson about: {topic}"
        else:
            # Generate a relevant topic based on specialization
            if specialization == "Theory":
                prompt = "Generate a lesson about a fundamental AI concept suitable for the user's level."
            elif specialization == "Tooling":
                prompt = "Generate a hands-on lesson about an AI development tool or practical technique."
            else:  # Hybrid
                prompt = "Generate a lesson that combines AI theory with practical implementation."
        
        prompt += "\n\nPlease structure your response as:\nTITLE: [lesson title]\nCONTENT: [lesson content]\nEXERCISE: [optional practice exercise]"
        
        return prompt
    
    def _parse_lesson_content(self, content: str) -> Dict[str, str]:
        """Parse the generated content into structured lesson data"""
        lines = content.split('\n')
        lesson = {
            "title": "AI Lesson",
            "content": content,
            "exercise": ""
        }
        
        current_section = "content"
        content_lines = []
        
        for line in lines:
            line = line.strip()
            if line.startswith("TITLE:"):
                lesson["title"] = line.replace("TITLE:", "").strip()
            elif line.startswith("CONTENT:"):
                current_section = "content"
                content_lines = []
            elif line.startswith("EXERCISE:"):
                lesson["content"] = "\n".join(content_lines).strip()
                current_section = "exercise"
                content_lines = []
            else:
                if current_section == "content":
                    content_lines.append(line)
                elif current_section == "exercise":
                    content_lines.append(line)
        
        if current_section == "content":
            lesson["content"] = "\n".join(content_lines).strip()
        elif current_section == "exercise":
            lesson["exercise"] = "\n".join(content_lines).strip()
        
        # Ensure we have content
        if not lesson["content"]:
            lesson["content"] = content
            
        return lesson
    
    def _generate_fallback_lesson(self, specialization: str, level: str, topic: str = None) -> Dict[str, str]:
        """Generate a fallback lesson when API fails"""
        import random
        
        fallback_lessons = {
            "Theory": {
                "Beginner": [
                    {
                        "title": "What is Artificial Intelligence?",
                        "content": """Artificial Intelligence (AI) is like teaching computers to think and make decisions, similar to how humans do, but in their own digital way.

**Key Concepts:**
1. **Intelligence**: The ability to learn, reason, and solve problems
2. **Artificial**: Created by humans, not naturally occurring
3. **Machine Learning**: A subset of AI where computers learn from examples
4. **Deep Learning**: A type of machine learning inspired by how our brains work

**Real-World Examples:**
- Voice assistants like Siri and Alexa recognizing speech
- Netflix recommending movies you might like
- Email filters detecting spam automatically
- GPS apps finding the best route to your destination

Think of AI as giving computers the ability to recognize patterns and make predictions, just like how you learned to recognize faces or predict traffic patterns.""",
                        "exercise": "Look around you and identify 3 AI systems you use daily. What patterns do you think they're recognizing?"
                    },
                    {
                        "title": "Machine Learning Basics",
                        "content": """Machine Learning is like teaching a computer to recognize patterns by showing it many examples.

**The Learning Process:**
1. **Data Collection**: Gather lots of examples (like photos of cats and dogs)
2. **Training**: Show the computer these examples with correct answers
3. **Pattern Recognition**: The computer finds common features and differences
4. **Prediction**: Use learned patterns to identify new, unseen examples

**Types of Machine Learning:**
- **Supervised Learning**: Learning with examples and correct answers
- **Unsupervised Learning**: Finding hidden patterns without correct answers
- **Reinforcement Learning**: Learning through trial and error with rewards

**Analogy**: It's like learning to drive:
- You observe many examples (supervised learning)
- You practice and get feedback (reinforcement learning)
- You develop intuition about traffic patterns (unsupervised learning)""",
                        "exercise": "Think of a skill you learned recently. How does your learning process compare to machine learning?"
                    }
                ],
                "Intermediate": [
                    {
                        "title": "Neural Networks and Deep Learning",
                        "content": """Neural Networks are computational models inspired by how neurons work in the human brain.

**Structure:**
- **Neurons (Nodes)**: Basic processing units that receive input, process it, and produce output
- **Layers**: Groups of neurons working together
  - Input Layer: Receives raw data
  - Hidden Layers: Process and transform information
  - Output Layer: Produces final results
- **Weights and Biases**: Parameters that determine how information flows

**Deep Learning:**
When neural networks have many hidden layers (typically 3+ layers), we call it "deep learning."

**Key Advantages:**
1. **Feature Learning**: Automatically discovers relevant patterns in data
2. **Scalability**: Performance improves with more data
3. **Versatility**: Works across many domains (vision, language, speech)

**Mathematical Foundation:**
Each neuron computes: output = activation(sum(inputs × weights) + bias)

**Applications:**
- Image recognition (CNNs)
- Language processing (Transformers)
- Game playing (AlphaGo)""",
                        "exercise": "Design a simple neural network for recognizing handwritten digits. What layers would you need?"
                    }
                ]
            },
            "Tooling": {
                "Beginner": [
                    {
                        "title": "Your First AI API Call with Python",
                        "content": """Let's build your first AI application using the OpenAI API!

**Setup:**
```bash
pip install openai
```

**Basic Implementation:**
```python
import openai

# Initialize the client
client = openai.OpenAI(api_key='your-api-key-here')

# Make your first API call
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain quantum computing in simple terms"}
    ]
)

print(response.choices[0].message.content)
```

**Key Components:**
1. **Client**: Your connection to the AI service
2. **Model**: The AI brain you're talking to
3. **Messages**: The conversation format
4. **Response**: The AI's answer

**Best Practices:**
- Always handle errors with try/except
- Set reasonable timeouts
- Monitor your API usage and costs""",
                        "exercise": "Modify the code to create a simple AI chatbot that answers questions about your favorite hobby."
                    },
                    {
                        "title": "Building AI Applications with Streamlit",
                        "content": """Streamlit makes it incredibly easy to create web interfaces for AI applications.

**Installation:**
```bash
pip install streamlit
```

**Simple AI Chat App:**
```python
import streamlit as st
import openai

st.title("My AI Assistant")

# User input
user_message = st.text_input("Ask me anything:")

if user_message:
    # AI response (simplified)
    with st.spinner("Thinking..."):
        # Your AI logic here
        ai_response = "This is where AI responds to: " + user_message
    
    st.write("AI:", ai_response)
```

**Run Your App:**
```bash
streamlit run app.py
```

**Streamlit Components:**
- `st.text_input()`: Get user input
- `st.button()`: Interactive buttons
- `st.selectbox()`: Dropdown menus
- `st.columns()`: Layout control
- `st.spinner()`: Loading indicators""",
                        "exercise": "Create a Streamlit app that takes a topic and generates quiz questions about it."
                    }
                ]
            },
            "Hybrid": [
                {
                    "title": "Understanding and Implementing Prompt Engineering",
                    "content": """Prompt Engineering combines AI theory with practical implementation skills.

**Theory: How AI Understands Prompts**
Language models like GPT work by predicting the next word based on patterns learned from vast text datasets. They don't "understand" like humans do, but they excel at pattern matching and completion.

**Practical Implementation:**
```python
# Basic prompt
basic_prompt = "Write a poem"

# Engineered prompt
engineered_prompt = \"\"\"
You are a professional poet specializing in haikus.
Write a haiku about technology that:
- Follows 5-7-5 syllable pattern
- Uses vivid imagery
- Conveys a sense of wonder

Topic: Artificial Intelligence
\"\"\"
```

**Key Techniques:**
1. **Role Playing**: "You are an expert in..."
2. **Context Setting**: Provide relevant background
3. **Format Specification**: Define expected output structure
4. **Few-Shot Learning**: Give examples

**Theory Behind It:**
- **Attention Mechanisms**: Models focus on relevant parts of your prompt
- **Context Windows**: Limited memory affects how much context the model can use
- **Training Bias**: Models reflect patterns from their training data

**Code Implementation:**
```python
def create_expert_prompt(domain, task, examples=None):
    prompt = f"You are a world-class expert in {domain}.\\n"
    prompt += f"Your task: {task}\\n"
    
    if examples:
        prompt += "Here are some examples:\\n"
        for i, example in enumerate(examples, 1):
            prompt += f"{i}. {example}\\n"
    
    return prompt
```""",
                    "exercise": "Design and implement a prompt engineering system for creating personalized learning content. Test it with different subjects."
                }
            ]
        }
        
        # Select appropriate lessons based on specialization and level
        if specialization in fallback_lessons:
            if level in fallback_lessons[specialization]:
                lessons = fallback_lessons[specialization][level]
                return random.choice(lessons)
            else:
                # Fallback to beginner lessons
                lessons = fallback_lessons[specialization].get("Beginner", fallback_lessons["Theory"]["Beginner"])
                return random.choice(lessons)
        else:
            # Default to Theory beginner
            return random.choice(fallback_lessons["Theory"]["Beginner"])

    def generate_alternative_explanation(self, original_content: str, feedback_type: str) -> str:
        """Generate alternative explanation based on user feedback"""
        
        # If no API key available, provide simple alternative
        if not self.has_api_key:
            return f"Let me explain this differently:\n\n{original_content}\n\nThink of it as a simple analogy - imagine you're explaining this concept to a friend who's never heard of it before. The key idea is to break it down into smaller, more digestible pieces and relate it to something familiar."
        
        try:
            prompt = f"""The user found this explanation {feedback_type}:
            
            "{original_content}"
            
            Please provide an alternative explanation that is:
            - Clearer and more accessible
            - Uses different analogies or examples
            - Breaks down complex parts further
            - More engaging and practical
            
            Keep the same core information but present it differently."""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are ProfeAI, an expert at explaining complex concepts in multiple ways. Adapt your teaching style based on student feedback."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.8
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Let me explain this differently: {original_content}\n\nTry thinking of it as a simple analogy - imagine you're explaining this concept to a friend who's never heard of it before."