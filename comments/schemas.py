from pydantic import BaseModel


class CommentCreate(BaseModel):
    content: str
    post_id: int


class Comment(BaseModel):
    id: int
    content: str
    post_id: int
    user_id: int

    class Config:
        orm_mode = True


class CommentAnalytics(BaseModel):
    date: str
    total_comments: int
    blocked_comments: int


class DeleteCommentResponse(BaseModel):
    message: str
    deleted_post: Comment
