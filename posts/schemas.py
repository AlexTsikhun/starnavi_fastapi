from pydantic import BaseModel


class PostCreate(BaseModel):
    title: str
    content: str


class Post(BaseModel):
    id: int
    title: str
    content: str
    owner_id: int

    class Config:
        orm_mode = True


class DeletePostResponse(BaseModel):
    message: str
    deleted_post: Post
