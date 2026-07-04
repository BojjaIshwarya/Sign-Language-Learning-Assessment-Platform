from fastapi import FastAPI

from app.database import engine, Base
from app import models
from app.routers import auth, users, learning, course

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sign Language Learning & Assessment Platform API",
    version="1.0.0",
    description="Backend API for Sign Language Learning & Assessment Platform"
)

# Include Routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(learning.router)
app.include_router(course.router)


@app.get("/")
def root():
    return {
        "message": "Welcome to Sign Language Learning & Assessment Platform API!"
    }
