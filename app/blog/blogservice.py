from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from config.get_db import get_db
from .models import Blog
from .schema import BlogBase
from fastapi_jwt_auth import AuthJWT
from users.models import User


class BlogService:
    def get_all(db: Session = Depends(get_db)):
        return db.query(Blog).filter(Blog.published == True).all()

    def create(
        request: BlogBase, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()
    ):

        try:
            Authorize.jwt_required()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
            )

        current_user = Authorize.get_jwt_subject()
        user = db.query(User).filter(User.email == current_user).first()

        new_blog = Blog(
            title=request.title,
            description=request.description,
            published=request.published,
        )

        new_blog.creator = user
        db.add(new_blog)
        db.commit()
        db.refresh(new_blog)
        return new_blog

    def update_blog(
        id: int,
        request: BlogBase,
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends(),
    ):
        try:
            Authorize.jwt_required()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
            )

        blog_update = db.query(Blog).filter(Blog.id == id).first()

        blog_update.title = request.title
        blog_update.description = request.description
        blog_update.published = request.published

        db.commit()

        return blog_update

    def delete_blog(
        id: int, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()
    ):
        try:
            Authorize.jwt_required()

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
            )

        blog_delete = db.query(Blog).filter(Blog.id == id).first()

        db.delete(blog_delete)

        db.commit()

        return blog_delete
