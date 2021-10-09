from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from fastapi_jwt_auth import AuthJWT

from comment.schema import CommentBase
from .models import Comment
from config.get_db import get_db
from blog.models import Blog

from users.models import User


class CommentService:
    def get_all(db: Session = Depends(get_db)):
        return db.query(Comment).all()

    def create_comment(
        id: int,
        request: CommentBase,
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends(),
    ):

        try:
            Authorize.jwt_required()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
            )
        # User
        current_user = Authorize.get_jwt_subject()
        user = db.query(User).filter(User.email == current_user).first()

        blog = db.query(Blog).filter(Blog.id == id).first()
        if not blog:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Blog with the id {id} is not available",
            )

        comment_b = Comment(description=request.description)
        comment_b.user_id = user.id

        db.add(comment_b)

        db.commit()

        blog.comment_id = comment_b.id

        db.commit()

        return comment_b

    def update_comment(
        idBlog: int,
        idComment: int,
        request: CommentBase,
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends(),
    ):
        try:
            Authorize.jwt_required()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
            )
        current_user = Authorize.get_jwt_subject()
        user = db.query(User).filter(User.email == current_user).first()

        blog_byid = db.query(Blog).filter(Blog.id == idBlog).first()

        if not blog_byid:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Comment with the id {id} is not available",
            )

        comment_byid = db.query(Comment).filter(Comment.id == idComment).first()

        if not comment_byid:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Blog with the id {id} is not available",
            )

        comment_byid.description = request.description
        comment_byid.user_id = user.id

        db.commit()

        return blog_byid

    def delete_comment(
        id: int,
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends(),
    ):
        try:
            Authorize.jwt_required()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
            )
        comment_del = db.query(Comment).filter(Comment.id == id).first()

        db.delete(comment_del)

        db.commit()

        return comment_del
