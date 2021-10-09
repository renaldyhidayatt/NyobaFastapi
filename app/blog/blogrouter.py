from fastapi import APIRouter, Depends, status
from fastapi_jwt_auth.auth_jwt import AuthJWT
from sqlalchemy.orm import Session
from config.get_db import get_db
from .blogservice import BlogService
from .schema import BlogBase

router = APIRouter(prefix="/blog", tags=["Blogs"])


@router.get("/")
def all(db: Session = Depends(get_db)):
    return BlogService.get_all(db)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
def create(
    request: BlogBase, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()
):
    return BlogService.create(request, db, Authorize)


@router.put("/{id}")
def update(
    id: int,
    request: BlogBase,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
):
    return BlogService.update_blog(id, request, db, Authorize)


@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    return BlogService.delete_blog(id, db, Authorize)
