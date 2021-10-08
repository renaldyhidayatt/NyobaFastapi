from pydantic import BaseModel


class BlogBase(BaseModel):
    title: str
    description: str
    published: bool
    comment_id: int


class BlogCreate(BlogBase):
    title: str
    description: str
    published: bool


class BlogUpdateComment(BaseModel):
    description: str
