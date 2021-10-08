from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from .commentservice import CommentService
from config.get_db import get_db

router = APIRouter(prefix="/comment", tags=["comments"])


@router.get("/")
def comment_list(db: Session = Depends(get_db)):
    return CommentService.get_all(db)


@router.post("/")
def comment_create(description, db: Session = Depends(get_db)):
    return CommentService.create_comment(description=description, db=db)
