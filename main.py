from fastapi import FastAPI, APIRouter

from comments import router as comments_router
from posts import router as posts_router
from user import router as user_router

app = FastAPI()

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(user_router.router)
api_router.include_router(posts_router.router)
api_router.include_router(comments_router.router)

app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
