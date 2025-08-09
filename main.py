#!/usr/bin/env python3
"""
ProfeAI - AI Professor with Emotional Intelligence
Main entry point for the application
"""

import uvicorn

if __name__ == "__main__":
    print("🤖 Starting ProfeAI - Your AI Professor with Emotional Intelligence")
    print("🌐 Open your browser to: http://localhost:8000")
    print("📚 Ready to learn AI theory, tooling, or both!")
    print("💡 ProfeAI adapts to your feedback and learning style")
    print()
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)