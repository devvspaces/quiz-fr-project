#!/usr/bin/env python3
"""
Script to generate sample quiz data for testing
"""

import requests
import json

API_BASE = "http://localhost:5000"

def get_admin_token():
    """Get admin authentication token"""
    response = requests.post(f"{API_BASE}/login", json={"password": "test"})
    if response.status_code == 200:
        return response.json()["token"]
    else:
        raise Exception("Failed to authenticate")

def create_question(token, question_data):
    """Create a new question"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{API_BASE}/questions", json=question_data, headers=headers)
    if response.status_code == 200:
        return response.json()["id"]
    else:
        raise Exception(f"Failed to create question: {response.text}")

def main():
    """Main function to create sample data"""
    print("Getting admin token...")
    token = get_admin_token()
    
    # Sample questions for a general knowledge quiz
    questions = [
        {
            "title": "Geography Question",
            "text": "What is the capital city of France?",
            "position": 1,
            "possibleAnswers": [
                {"text": "London", "isCorrect": False},
                {"text": "Berlin", "isCorrect": False},
                {"text": "Paris", "isCorrect": True},
                {"text": "Madrid", "isCorrect": False}
            ]
        },
        {
            "title": "Science Question",
            "text": "What is the chemical symbol for gold?",
            "position": 2,
            "possibleAnswers": [
                {"text": "Go", "isCorrect": False},
                {"text": "Au", "isCorrect": True},
                {"text": "Ag", "isCorrect": False},
                {"text": "Gd", "isCorrect": False}
            ]
        },
        {
            "title": "History Question",
            "text": "In which year did World War II end?",
            "position": 3,
            "possibleAnswers": [
                {"text": "1944", "isCorrect": False},
                {"text": "1945", "isCorrect": True},
                {"text": "1946", "isCorrect": False},
                {"text": "1947", "isCorrect": False}
            ]
        },
        {
            "title": "Mathematics Question",
            "text": "What is the square root of 64?",
            "position": 4,
            "possibleAnswers": [
                {"text": "6", "isCorrect": False},
                {"text": "7", "isCorrect": False},
                {"text": "8", "isCorrect": True},
                {"text": "9", "isCorrect": False}
            ]
        },
        {
            "title": "Literature Question",
            "text": "Who wrote the novel '1984'?",
            "position": 5,
            "possibleAnswers": [
                {"text": "Aldous Huxley", "isCorrect": False},
                {"text": "George Orwell", "isCorrect": True},
                {"text": "Ray Bradbury", "isCorrect": False},
                {"text": "H.G. Wells", "isCorrect": False}
            ]
        }
    ]
    
    print("Creating sample questions...")
    for i, question in enumerate(questions, 1):
        try:
            question_id = create_question(token, question)
            print(f"Created question {i}: '{question['title']}' (ID: {question_id})")
        except Exception as e:
            print(f"Error creating question {i}: {e}")
    
    print("Sample data creation complete!")

if __name__ == "__main__":
    main()