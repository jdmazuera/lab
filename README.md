# FastAPI with PostgreSQL Docker Setup

This project provides a complete Docker Compose setup with a FastAPI application and PostgreSQL database.

## Architecture

- **FastAPI Service**: Python service with FastAPI, Pydantic, and SQLAlchemy
- **PostgreSQL Database**: PostgreSQL 15 with port 5432 exposed
- **Docker Compose**: Orchestrates both services with proper networking

## Files Structure

- `docker-compose.yml`: Main orchestration file
- `Dockerfile`: Python FastAPI container configuration
- `requirements.txt`: Python dependencies
- `main.py`: FastAPI application with SQLAlchemy models
- `.env`: Environment configuration
- `README.md`: This documentation

## Quick Start

1. **Build and run the services:**
   ```bash
   docker-compose up --build
   ```

2. **Access the services:**
   - FastAPI Application: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - PostgreSQL: localhost:5432

## API Endpoints

- `GET /`: Health check endpoint
- `GET /health`: Detailed health check
- `POST /users/`: Create a new user
- `GET /users/`: Get all users
- `GET /users/{user_id}`: Get specific user by ID
- `DELETE /users/{user_id}`: Delete a user

## Database Configuration

The PostgreSQL database is configured with:
- **Database**: appdb
- **User**: postgres
- **Password**: password
- **Port**: 5432 (exposed to host)

## Development

To run locally for development:

1. Install dependencies: `pip install -r requirements.txt`
2. Set environment variables from `.env` file
3. Run the FastAPI server: `uvicorn main:app --reload`

## Stopping the Services

```bash
docker-compose down
```

To remove volumes (including database data):
```bash
docker-compose down -v