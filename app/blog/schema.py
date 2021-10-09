from typing import Optional
from pydantic import BaseModel


class BlogBase(BaseModel):
    title: str
    description: str
    published: Optional[bool]
