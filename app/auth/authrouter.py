from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth.auth_jwt import AuthJWT

from sqlalchemy.orm import Session

from auth.authservice import AuthService

from .schema import LoginModel, SignUpModel
from config.get_db import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/")
def testingJwt(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
        )

    return {"user": Authorize.get_jwt_subject()}


@router.post("/register")
def registerUser(user: SignUpModel, db: Session = Depends(get_db)):

    return AuthService.register_user(user=user, db=db)


@router.post("/login")
def loginUser(
    user: LoginModel, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()
):
    return AuthService.login_user(user=user, Authorize=Authorize, db=db)
