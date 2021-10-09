from typing import Optional
from pydantic import BaseModel


class CommentBase(BaseModel):
    id: Optional[int]
    description: str
