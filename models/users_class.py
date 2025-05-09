from pydantic import BaseModel, Field, EmailStr
class User(BaseModel):
    id: int 
    name: str = Field(min_length=2, description="El nombre debe contener al menos dos letras")
    email: EmailStr
    birthdate: str
    disabled: bool 
    
class UserUpdate(BaseModel):
    id: int | None = None
    name: str | None = None
    email: EmailStr| None = None
    birthdate: str| None = None
    disabled: bool | None = None

class UserDB(User):
    password: str 