from typing import Optional
from pydantic import BaseModel


class SignUpModel(BaseModel):
    name: str
    email: str
    password: Optional[str]
    is_staff: Optional[bool]
    is_active: Optional[bool]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "johndoe",
                "email": "johndoe@gmail.com",
                "password": "password",
                "is_staff": False,
                "is_active": True,
            }
        }


class LoginModel(BaseModel):
    email: str
    password: str


class Settings(BaseModel):
    authjwt_secret_key: str = (
        "b4bb9013c1c03b29b9311ec0df07f3b0d8fd13edd02d5c45b2fa7b86341fa405"
    )
