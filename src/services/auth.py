from datetime import datetime, timedelta, timezone
from src.config.setting import Settings
from jose import jwt
from src.domains.users.repositories import UserRepository
from src.domains.users.services import verify_password
from fastapi import HTTPException, Depends, status
from jose.exceptions import JWTError
from jose.exceptions import ExpiredSignatureError
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def validate_token(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, Settings().JWT_SECRET_KEY, algorithms=Settings().ALGORITHM)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credentials expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise credentials_exception


def authenticate_user(email: str, password: str, db):
    user_repo = UserRepository(db)
    user = user_repo.get_by_email(email=email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Settings().JWT_SECRET_KEY, algorithm=Settings().ALGORITHM)
    return encoded_jwt
