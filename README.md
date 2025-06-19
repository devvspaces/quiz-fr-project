# Quiz Application

A full-stack web application built with Python Flask backend and Vue.js frontend for creating and taking quizzes.

## Project Structure

```
quiz-app/
├── quiz-api/          # Python Flask backend
│   ├── app.py         # Main Flask application
│   ├── jwt_utils.py   # JWT token utilities
│   ├── requirements.txt
│   └── venv/          # Python virtual environment
└── quiz-ui/           # Vue.js frontend
    ├── src/
    │   ├── components/    # Vue components
    │   ├── services/      # API service layer
    │   ├── views/         # Page components
    │   └── router/        # Vue router configuration
    └── package.json
```

## Features

### Frontend (Public)
- **Home Page**: Welcome page with leaderboard of best scores
- **Quiz Participation**: Multi-step quiz with progress tracking
- **Score Display**: Results page with score and ranking

### Backend API
- RESTful API with SQLite database
- JWT-based authentication for admin functions
- CORS enabled for frontend integration

### Admin Interface
- Password-protected admin area
- Create, edit, and delete questions
- Manage question order and content
- Image upload support for questions

## Setup Instructions

### Backend Setup

1. Navigate to the quiz-api directory:
```bash
cd quiz-app/quiz-api
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the Flask application:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

### Frontend Setup

1. Navigate to the quiz-ui directory:
```bash
cd quiz-app/quiz-ui
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## API Endpoints

### Public Endpoints
- `GET /quiz-info` - Get quiz information and past scores
- `GET /questions/{id}` - Get question by ID
- `GET /questions?position={position}` - Get question by position
- `POST /participations` - Submit quiz answers
- `POST /login` - Admin login

### Admin Endpoints (Authenticated)
- `POST /questions` - Create new question
- `PUT /questions/{id}` - Update question
- `DELETE /questions/{id}` - Delete question
- `DELETE /questions/all` - Delete all questions
- `DELETE /participations/all` - Delete all participations
- `POST /rebuild-db` - Rebuild database schema

## Default Admin Credentials

- Password: `test` (MD5 hash: `098f6bcd4621d373cade4e832627b4f6`)

## Database Schema

The application uses SQLite with the following tables:

### Questions
- id (INTEGER PRIMARY KEY)
- title (TEXT)
- text (TEXT)
- image (TEXT) - Base64 encoded image
- position (INTEGER) - Order in quiz

### Answers
- id (INTEGER PRIMARY KEY)
- question_id (INTEGER)
- text (TEXT)
- isCorrect (BOOLEAN)

### Participations
- id (INTEGER PRIMARY KEY)
- playerName (TEXT)
- score (INTEGER)
- date (TEXT)

## Technologies Used

### Backend
- Python 3
- Flask web framework
- SQLite database
- JWT for authentication
- Flask-CORS for cross-origin requests
- PyJWT for token handling

### Frontend
- Vue.js 3 with Composition API
- Vue Router for navigation
- Axios for HTTP requests
- Bootstrap 5 for styling
- Vite for build tooling

## Development Notes

- The application follows the Vue.js Composition API pattern
- All API requests are handled through the QuizApiService
- Local storage is used for session management
- Images are stored as base64 strings in the database
- The admin password is stored as MD5 hash for basic security

## Testing

To test the application:

1. Start both backend and frontend servers
2. Visit `http://localhost:3000`
3. Create questions in the admin interface (login with password: `test`)
4. Take the quiz as a regular user
5. View scores on the home page

## Production Deployment

For production deployment:

1. Set proper environment variables
2. Use a production WSGI server (e.g., Gunicorn) for Flask
3. Build the frontend for production: `npm run build`
4. Serve static files with a web server (e.g., Nginx)
5. Use a proper database (PostgreSQL/MySQL) instead of SQLite
6. Implement proper secret management for JWT tokens