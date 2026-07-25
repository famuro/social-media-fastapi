from fastapi import FastAPI


app: FastAPI = FastAPI(
    title="Social Media API",
    description="A social media backend API.",
    version="0.1.0",
)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello world from the Social Media API"}
