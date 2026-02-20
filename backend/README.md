# FinTrace AI - Backend

This is the FastAPI backend for the FinTrace AI fraud detection system.

## Deployment Instructions

### Environment Variables
Ensure the following environment variable is set in your deployment platform:
- `GROQ_API_KEY`: Your Groq API key for AI summaries.

### Local Run
1. Install dependencies: `pip install -r requirements.txt`
2. Run server: `uvicorn app.main:app --reload`

### Production Run (via uvicorn)
`uvicorn app.main:app --host 0.0.0.0 --port 8000`

### Docker Deployment
1. Build: `docker build -t fintrace-backend .`
2. Run: `docker run -p 8000:8000 --env-file .env fintrace-backend`
