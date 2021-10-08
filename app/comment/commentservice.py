from fastapi import Depends
from sqlalchemy.orm import Session
from .models import Comment
from config.get_db import get_db


class CommentService:
    def get_all(db: Session = Depends(get_db)):
        return db.query(Comment).all()

    def create_comment(description: str, db: Session = Depends(get_db)):
        comment = Comment(description=description)

        db.add(comment)

        db.commit()

        db.refresh(comment)

        return comment
