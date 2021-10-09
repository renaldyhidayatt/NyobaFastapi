from fastapi import APIRouter, status, Depends
from fastapi_jwt_auth.auth_jwt import AuthJWT
from sqlalchemy.orm import Session
from auth.schema import SignUpModel
from users.usersservice import UsersService
from config.get_db import get_db


router = APIRouter(prefix="/users", tags=["USers"])


@router.get("/")
def GetAll(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    return UsersService.get_all(db, Authorize=Authorize)


@router.post("/")
def createUser(
    user: SignUpModel, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()
):
    return UsersService.create_user(user, db, Authorize=Authorize)


@router.put("/{id}")
def updateUser(id: int, user: SignUpModel, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    return UsersService.update_user(id, user, db, Authorize=Authorize)


@router.delete("/{id}")
def deleteUser(id: int, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    return UsersService.delete_user(id, db, Authorize)
