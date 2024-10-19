from fastapi import FastAPI
from user import router as user_router
from posts import router as posts_router
from comments import router as comments_router

app = FastAPI()

app.include_router(user_router.router)
app.include_router(posts_router.router)
app.include_router(comments_router.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
