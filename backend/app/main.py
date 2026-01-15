# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api import memory
from app.api import evolution
from app.api import graph
from app.api import brain   

app = FastAPI(
    title=settings.PROJECT_NAME
)

# CORS (REQUIRED)
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

# Root health check
@app.get("/")
def root():
    return {"status": "Memora OS backend running"}

# API routers
app.include_router(memory.router, prefix=settings.API_V1_STR)
app.include_router(evolution.router, prefix=settings.API_V1_STR)
app.include_router(graph.router, prefix=settings.API_V1_STR)
app.include_router(brain.router, prefix=settings.API_V1_STR)  
