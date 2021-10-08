from fastapi import Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from users.models import User
from auth.schema import LoginModel, SignUpModel
from config.get_db import get_db
from config.hashing import Hashing


class AuthService:
    def register_user(user: SignUpModel, db: Session = Depends(get_db)):
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

    def login_user(
        user: LoginModel, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)
    ):
        db_email = db.query(User).filter(User.email == user.email).first()

        if db_email and Hashing.verify_hash(db_email.password, user.password):
            access_token = Authorize.create_access_token(subject=db_email.email)

            response = {"access": access_token}
            return jsonable_encoder(response)

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email Or Password"
        )
