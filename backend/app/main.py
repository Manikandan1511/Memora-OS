from fastapi import FastAPI
from app.core.config import settings
from app.api import memory

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(memory.router, prefix=settings.API_V1_STR)

@app.get("/")
def health_check():
    return {
        "status": "ok",
        "message": "Memora OS backend is running 🚀"
    }
