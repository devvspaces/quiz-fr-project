# Database Schema

## Entity Relationship Diagram

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│   QUESTIONS     │       │     ANSWERS     │       │ PARTICIPATIONS  │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ id (PK)         │◄─────┐│ id (PK)         │       │ id (PK)         │
│ title           │      └│ question_id (FK)│       │ playerName      │
│ text            │       │ text            │       │ score           │
│ image           │       │ isCorrect       │       │ date            │
│ position        │       └─────────────────┘       └─────────────────┘
└─────────────────┘
```

## Table Definitions

### QUESTIONS
Stores quiz questions with their metadata.

| Column   | Type    | Constraints           | Description                    |
|----------|---------|----------------------|--------------------------------|
| id       | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique question identifier     |
| title    | TEXT    | NOT NULL             | Question title/category        |
| text     | TEXT    | NOT NULL             | The actual question text       |
| image    | TEXT    | NULL                 | Base64 encoded image (optional)|
| position | INTEGER | NOT NULL, UNIQUE     | Order position in quiz         |

### ANSWERS
Stores possible answers for each question.

| Column      | Type    | Constraints                    | Description                    |
|-------------|---------|-------------------------------|--------------------------------|
| id          | INTEGER | PRIMARY KEY, AUTOINCREMENT    | Unique answer identifier       |
| question_id | INTEGER | NOT NULL, FOREIGN KEY         | Reference to questions.id      |
| text        | TEXT    | NOT NULL                      | Answer text                    |
| isCorrect   | BOOLEAN | NOT NULL                      | True if this is correct answer |

### PARTICIPATIONS
Stores quiz completion records and scores.

| Column     | Type    | Constraints           | Description                    |
|------------|---------|----------------------|--------------------------------|
| id         | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique participation ID        |
| playerName | TEXT    | NOT NULL             | Name of the quiz participant   |
| score      | INTEGER | NOT NULL             | Final score achieved           |
| date       | TEXT    | NOT NULL             | Completion date (DD/MM/YYYY HH:MM:SS) |

## Relationships

- **Questions → Answers**: One-to-Many
  - One question can have multiple answers (typically 4)
  - Foreign key: `answers.question_id` → `questions.id`
  - Cascade delete: When a question is deleted, all its answers are deleted

- **Questions ← Participations**: Implicit relationship
  - Participations store the final score but not individual answer selections
  - The relationship is maintained through the business logic in the API

## Constraints and Business Rules

1. **Question Position**: Must be unique and sequential starting from 1
2. **Answer Count**: Each question should have exactly 4 answers
3. **Correct Answer**: Each question must have exactly one correct answer
4. **Image Storage**: Images are stored as base64 encoded strings
5. **Score Calculation**: Score equals the number of correct answers
6. **Date Format**: Stored as string in format "DD/MM/YYYY HH:MM:SS"

## Sample Data

The database can be populated with sample questions using the provided `sample_data.py` script:

```bash
python3 sample_data.py
```

This creates 6 sample questions covering:
- Geography (Capital of France)
- Science (Chemical symbol for gold)
- History (End of WWII)
- Mathematics (Square root of 64)
- Literature (Author of 1984)
- Basic arithmetic (2+2)

## Database Initialization

The database schema is automatically created when the Flask application starts for the first time. The `init_db()` function in `app.py` handles table creation with proper foreign key constraints.

For manual database reset, use the admin endpoint:
```bash
POST /rebuild-db
Authorization: Bearer <admin_token>
```