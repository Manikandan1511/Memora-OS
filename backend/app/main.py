# backend/app/main.py

from fastapi import FastAPI
from app.core.config import settings

from app.api import memory
from app.api import graph

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(memory.router, prefix=settings.API_V1_STR)
app.include_router(graph.router, prefix=settings.API_V1_STR)


@app.get("/")
def root():
    return {"status": "Memora OS backend running"}
