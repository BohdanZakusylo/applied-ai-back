# AI Healthcare Assistant - Backend API

REST API for the AI Healthcare Assistant focused on Dutch insurance matters for international students.

## Project Structure

```
applied-ai-back/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── app/
│   ├── config.py          # Application configuration
│   ├── models/            # Pydantic models for request/response
│   │   ├── auth.py        # Authentication models
│   │   ├── user.py        # User profile models
│   │   ├── chat.py        # Chat/AI models
│   │   └── file.py        # File upload models
│   ├── routers/           # API route definitions
│   │   ├── auth.py        # Authentication endpoints
│   │   ├── users.py       # User profile endpoints
│   │   ├── chat.py        # AI chat endpoints
│   │   ├── files.py       # File upload endpoints
│   │   └── health.py      # Health check endpoint
│   └── services/          # Business logic (placeholder)
│       ├── auth_service.py
│       ├── user_service.py
│       ├── chat_service.py
│       └── file_service.py
```

## Setup

1. **Activate virtual environment:**
   ```bash
   source .venv/bin/activate  # On macOS/Linux
   # or
   .venv\Scripts\activate     # On Windows
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment variables:**
   Create a `.env` file with the following variables:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/ai_healthcare_db
   SECRET_KEY=your-super-secret-jwt-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   OPENAI_API_KEY=your-openai-api-key-here
   MAX_FILE_SIZE=10485760
   UPLOAD_DIR=uploads
   ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
   ```

4. **Run the server:**
   ```bash
   uvicorn main:app --reload
   ```

## API Endpoints

### Authentication (`/auth`)
- `POST /auth/register` - Register new user
- `POST /auth/login` - User login
- `POST /auth/refresh` - Refresh JWT token
- `POST /auth/logout` - User logout
- `POST /auth/forgot-password` - Request password reset
- `POST /auth/reset-password` - Reset password

### Users (`/users`)
- `GET /users/profile` - Get user profile
- `PUT /users/profile` - Update user profile
- `DELETE /users/profile` - Delete user account

### Chat (`/chat`)
- `POST /chat/message` - Send message to AI
- `GET /chat/history` - Get conversation history
- `DELETE /chat/history` - Clear chat history

### Files (`/files`)
- `POST /files/upload` - Upload insurance documents
- `GET /files/{file_id}` - Get file information
- `DELETE /files/{file_id}` - Delete file

### Health
- `GET /health` - API health status

## Documentation

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Notes

- All endpoints are currently **placeholder implementations**
- JWT authentication logic needs to be implemented
- Database models and connections need to be set up
- OpenAI API integration needs to be implemented
- File upload storage needs to be configured
- This is the initial API structure for the first sprint