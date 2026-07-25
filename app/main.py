from fastapi import FastAPI

from app.core.config import settings


app: FastAPI = FastAPI(
    title=settings.app_name,
    description="A social media backend API.",
    version="0.1.0",
)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello world from the Social Media API"}
