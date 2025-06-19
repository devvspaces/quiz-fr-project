from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import hashlib
import base64
import os
from jwt_utils import build_token, decode_token
from functools import wraps

app = Flask(__name__)
CORS(app)

DATABASE = 'quiz.db'
ADMIN_PASSWORD_HASH = "098f6bcd4621d373cade4e832627b4f6"  # MD5 hash of "test"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    
    # Create questions table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            text TEXT NOT NULL,
            image TEXT,
            position INTEGER NOT NULL UNIQUE
        )
    ''')
    
    # Create answers table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER NOT NULL,
            text TEXT NOT NULL,
            isCorrect BOOLEAN NOT NULL,
            FOREIGN KEY (question_id) REFERENCES questions (id) ON DELETE CASCADE
        )
    ''')
    
    # Create participations table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS participations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            playerName TEXT NOT NULL,
            score INTEGER NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        if token.startswith('Bearer '):
            token = token.split(' ')[1]
        
        user_id = decode_token(token)
        if isinstance(user_id, str):  # Error message
            return jsonify({'error': user_id}), 401
        
        return f(*args, **kwargs)
    return decorated_function

@app.route('/rebuild-db', methods=['POST'])
@require_auth
def rebuild_db():
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
    init_db()
    return '', 204

@app.route('/quiz-info', methods=['GET'])
def get_quiz_info():
    conn = get_db_connection()
    
    # Get number of questions
    size = conn.execute('SELECT COUNT(*) as count FROM questions').fetchone()['count']
    
    # Get past scores
    scores = conn.execute('''
        SELECT playerName, score, date 
        FROM participations 
        ORDER BY score DESC, date DESC
    ''').fetchall()
    
    conn.close()
    
    return jsonify({
        'size': size,
        'scores': [dict(score) for score in scores]
    })

@app.route('/questions/<int:question_id>', methods=['GET'])
def get_question_by_id(question_id):
    conn = get_db_connection()
    
    question = conn.execute('''
        SELECT id, title, text, image, position 
        FROM questions 
        WHERE id = ?
    ''', (question_id,)).fetchone()
    
    if not question:
        conn.close()
        return jsonify({'error': 'Question not found'}), 404
    
    answers = conn.execute('''
        SELECT id, text, isCorrect 
        FROM answers 
        WHERE question_id = ?
    ''', (question_id,)).fetchall()
    
    conn.close()
    
    return jsonify({
        'id': question['id'],
        'title': question['title'],
        'text': question['text'],
        'image': question['image'],
        'position': question['position'],
        'possibleAnswers': [dict(answer) for answer in answers]
    })

@app.route('/questions', methods=['GET'])
def get_question_by_position():
    position = request.args.get('position', type=int)
    if position is None:
        return jsonify({'error': 'Position parameter is required'}), 400
    
    conn = get_db_connection()
    
    question = conn.execute('''
        SELECT id, title, text, image, position 
        FROM questions 
        WHERE position = ?
    ''', (position,)).fetchone()
    
    if not question:
        conn.close()
        return jsonify({'error': 'Question not found'}), 404
    
    answers = conn.execute('''
        SELECT id, text, isCorrect 
        FROM answers 
        WHERE question_id = ?
    ''', (question['id'],)).fetchall()
    
    conn.close()
    
    return jsonify({
        'id': question['id'],
        'title': question['title'],
        'text': question['text'],
        'image': question['image'],
        'position': question['position'],
        'possibleAnswers': [dict(answer) for answer in answers]
    })

@app.route('/participations', methods=['POST'])
def submit_participation():
    data = request.get_json()
    
    if not data or 'playerName' not in data or 'answers' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    player_name = data['playerName']
    answers = data['answers']
    
    conn = get_db_connection()
    
    # Get all questions with their correct answers
    questions = conn.execute('''
        SELECT q.id, q.position, a.id as answer_id
        FROM questions q
        JOIN answers a ON q.id = a.question_id
        WHERE a.isCorrect = 1
        ORDER BY q.position
    ''').fetchall()
    
    if len(answers) != len(questions):
        conn.close()
        return jsonify({'error': 'Invalid number of answers'}), 400
    
    # Calculate score
    score = 0
    answers_summaries = []
    
    for i, question in enumerate(questions):
        correct_answer_id = question['answer_id']
        player_answer_id = answers[i]
        was_correct = correct_answer_id == player_answer_id
        
        if was_correct:
            score += 1
        
        # Get correct answer position (1-4)
        all_answers = conn.execute('''
            SELECT id FROM answers 
            WHERE question_id = ?
            ORDER BY id
        ''', (question['id'],)).fetchall()
        
        correct_answer_position = next((i + 1 for i, ans in enumerate(all_answers) if ans['id'] == correct_answer_id), 1)
        
        answers_summaries.append({
            'correctAnswerPosition': correct_answer_position,
            'wasCorrect': was_correct
        })
    
    # Save participation
    from datetime import datetime
    date_str = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    
    conn.execute('''
        INSERT INTO participations (playerName, score, date)
        VALUES (?, ?, ?)
    ''', (player_name, score, date_str))
    
    conn.commit()
    conn.close()
    
    return jsonify({
        'answersSummaries': answers_summaries,
        'playerName': player_name,
        'score': score
    })

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or 'password' not in data:
        return jsonify({'error': 'Password is required'}), 400
    
    password = data['password']
    password_hash = hashlib.md5(password.encode()).hexdigest()
    
    if password_hash == ADMIN_PASSWORD_HASH:
        token = build_token()
        return jsonify({'token': token})
    else:
        return 'Unauthorized', 401

@app.route('/questions', methods=['POST'])
@require_auth
def create_question():
    data = request.get_json()
    
    if not data or 'title' not in data or 'text' not in data or 'position' not in data or 'possibleAnswers' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = get_db_connection()
    
    # Check if position already exists and shift positions if necessary
    existing = conn.execute('SELECT id FROM questions WHERE position >= ?', (data['position'],)).fetchall()
    if existing:
        conn.execute('UPDATE questions SET position = position + 1 WHERE position >= ?', (data['position'],))
    
    # Insert question
    cursor = conn.execute('''
        INSERT INTO questions (title, text, image, position)
        VALUES (?, ?, ?, ?)
    ''', (data['title'], data['text'], data.get('image'), data['position']))
    
    question_id = cursor.lastrowid
    
    # Insert answers
    for answer in data['possibleAnswers']:
        conn.execute('''
            INSERT INTO answers (question_id, text, isCorrect)
            VALUES (?, ?, ?)
        ''', (question_id, answer['text'], answer['isCorrect']))
    
    conn.commit()
    conn.close()
    
    return jsonify({'id': question_id})

@app.route('/questions/<int:question_id>', methods=['PUT'])
@require_auth
def update_question(question_id):
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    conn = get_db_connection()
    
    # Update question
    conn.execute('''
        UPDATE questions 
        SET title = ?, text = ?, image = ?, position = ?
        WHERE id = ?
    ''', (data['title'], data['text'], data.get('image'), data['position'], question_id))
    
    # Delete existing answers
    conn.execute('DELETE FROM answers WHERE question_id = ?', (question_id,))
    
    # Insert new answers
    for answer in data['possibleAnswers']:
        conn.execute('''
            INSERT INTO answers (question_id, text, isCorrect)
            VALUES (?, ?, ?)
        ''', (question_id, answer['text'], answer['isCorrect']))
    
    conn.commit()
    conn.close()
    
    return '', 204

@app.route('/questions/<int:question_id>', methods=['DELETE'])
@require_auth
def delete_question(question_id):
    conn = get_db_connection()
    
    # Get the position of the question to be deleted
    question = conn.execute('SELECT position FROM questions WHERE id = ?', (question_id,)).fetchone()
    if not question:
        conn.close()
        return jsonify({'error': 'Question not found'}), 404
    
    position = question['position']
    
    # Delete the question (answers will be deleted automatically due to CASCADE)
    conn.execute('DELETE FROM questions WHERE id = ?', (question_id,))
    
    # Shift positions down for questions after the deleted one
    conn.execute('UPDATE questions SET position = position - 1 WHERE position > ?', (position,))
    
    conn.commit()
    conn.close()
    
    return '', 204

@app.route('/questions/all', methods=['DELETE'])
@require_auth
def delete_all_questions():
    conn = get_db_connection()
    conn.execute('DELETE FROM questions')
    conn.commit()
    conn.close()
    return '', 204

@app.route('/participations/all', methods=['DELETE'])
@require_auth
def delete_all_participations():
    conn = get_db_connection()
    conn.execute('DELETE FROM participations')
    conn.commit()
    conn.close()
    return '', 204

if __name__ == "__main__":
    init_db()
    app.run(debug=True)