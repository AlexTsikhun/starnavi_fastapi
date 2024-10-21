from fastapi import FastAPI

from comments import router as comments_router
from posts import router as posts_router
from user import router as user_router

app = FastAPI()

app.include_router(user_router.router, prefix="/api/v1")
app.include_router(posts_router.router, prefix="/api/v1")
app.include_router(comments_router.router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Hello World"}
