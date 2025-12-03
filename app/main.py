from database import Base, engine
from fastapi import FastAPI
from api import router

# FastAPI app
app = FastAPI(title="FastAPI with PostgreSQL", version="1.0.0")

# Include API router
app.include_router(router)

# Create tables
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)