from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from comment.schema import CommentBase

from .commentservice import CommentService
from config.get_db import get_db

router = APIRouter(prefix="/comment", tags=["comments"])


@router.get("/")
def comment_list(db: Session = Depends(get_db)):
    return CommentService.get_all(db)


@router.post("/{id}")
def comment_create(
    id: int,
    request: CommentBase,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
):
    return CommentService.create_comment(
        id, request=request, db=db, Authorize=Authorize
    )


@router.put("/{idBlog}/{idComment}")
def comment_update(
    idBlog: int,
    idComment: int,
    request: CommentBase,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
):
    return CommentService.update_comment(
        idBlog=idBlog, idComment=idComment, request=request, db=db, Authorize=Authorize
    )


@router.delete("/{id}")
def comment_delete(
    id: int,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
):
    return CommentService.delete_comment(id, db, Authorize)
