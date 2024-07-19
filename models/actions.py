from models.core import CoreModel
from pydantic import EmailStr


class ActionUserLogin(CoreModel):
    user_email: EmailStr
    password: str