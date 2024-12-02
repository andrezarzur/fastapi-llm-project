from fastapi.security import OAuth2PasswordBearer
from src.config.database import Session
from fastapi import Depends
from src.services.auth import validate_token


def get_oauth2_scheme():
    return OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


def validate_token_dependency(token: str = Depends(get_oauth2_scheme())):
    validate_token(token)

