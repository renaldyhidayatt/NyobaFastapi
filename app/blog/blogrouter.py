from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from blog.schemas import BlogUpdateComment

from .blogservice import BlogService
from config.get_db import get_db


router = APIRouter(prefix="/blog", tags=["blogs"])


@router.get("/")
def blog_list(db: Session = Depends(get_db)):
    return BlogService.get_all(db)


@router.post("/")
def blog_create(
    title: str,
    description: str,
    published: bool,
    db: Session = Depends(get_db),
):
    return BlogService.create_blog(
        title=title,
        description=description,
        published=published,
        db=db,
    )


@router.get("/{id}", status_code=200)
def blog_byid(id: int, db: Session = Depends(get_db)):
    return BlogService.show_blog(id=id, db=db)


@router.post("/{id}/comment")
def blog_comment(id: int, description: str, db: Session = Depends(get_db)):
    return BlogService.show_comment(id=id, description=description, db=db)
