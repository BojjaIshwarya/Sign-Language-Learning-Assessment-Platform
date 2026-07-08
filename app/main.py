from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app import models
from app.routers import (
    auth,
    users,
    learning,
    course,
    assessment,
    ai
)

app = FastAPI(
    title="Sign Language Learning & Assessment Platform API",
    version="1.0.0",
    description="Backend API for Sign Language Learning & Assessment Platform"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)


# Include Routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(learning.router)
app.include_router(course.router)
app.include_router(ai.router)
app.include_router(assessment.router)


@app.get("/")
def root():
    return {
        "message": "Welcome to Sign Language Learning & Assessment Platform API!"
    }
