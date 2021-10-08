from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from blog.schemas import BlogUpdateComment

from comment.commentservice import CommentService
from comment.models import Comment
from .models import Blog
from config.get_db import get_db


class BlogService:
    def get_all(db: Session = Depends(get_db)):

        return db.query(Blog).all()

    def create_blog(
        title: str,
        description: str,
        published: bool,
        db: Session = Depends(get_db),
    ):
        blog = Blog(title=title, description=description, published=published)

        db.add(blog)
        db.commit()

        db.refresh(blog)

        return blog

    def show_blog(id: int, db: Session):
        blog = db.query(Blog).filter(Blog.id == id).first()

        if not blog:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Blog with the id {id} is not available",
            )

        return blog

    def show_comment(id: int, description: str, db: Session = Depends(get_db)):
        comment_create = CommentService.create_comment(description=description, db=db)

        db.add(comment_create)
        db.commit()
        db.refresh(comment_create)

        comment_id = (
            db.query(Comment).filter(Comment.description == description).first()
        )

        if not comment_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Comment with the id {id} is not available",
            )

        blog = db.query(Blog).filter(Blog.id == id).first()

        blog.comment_id = comment_id.id

        db.commit()
        print(comment_id.id)
        return "Update kayak nya"


## Lanjut lagi
