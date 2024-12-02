from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    fantasy_name: str
    cnpj: str
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    fantasy_name: str or None = None
    cnpj: str or None = None
    email: EmailStr or None = None
    password: str or None = None
