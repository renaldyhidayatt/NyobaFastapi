from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from .models import User
from config.get_db import get_db
from auth.schema import SignUpModel
from config.hashing import Hashing
from fastapi_jwt_auth import AuthJWT


class UsersService:
    def get_all(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
        try:
            Authorize.jwt_required()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
            )

        return db.query(User).all()

    def create_user(
        user: SignUpModel, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()
    ):

        try:
            Authorize.jwt_required()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
            )
        db_email = db.query(User).filter(User.email == user.email).first()

        if db_email is not None:
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with email already exits",
            )

        new_user = User(
            name=user.name,
            email=user.email,
            password=Hashing.hash_password(user.password),
            is_active=user.is_active,
            is_staff=user.is_staff,
        )

        db.add(new_user)

        db.commit()

        return new_user

    def update_user(
        id: int,
        user: SignUpModel,
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends(),
    ):
        try:
            Authorize.jwt_required()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
            )

        user_byid = db.query(User).filter(User.id == id).first()

        if not user_byid:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"USer with the id {id} is not available",
            )

        user_byid.name = user.name
        user_byid.email = user.email
        user_byid.is_staff = user.is_staff
        user_byid.is_active = user.is_active

        db.commit()

        return user_byid

    def delete_user(id: int, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
        try:
            Authorize.jwt_required()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
            )

        user_del = db.query(User).filter(User.id == id).first()

        db.delete(user_del)

        db.commit()

        return user_del
