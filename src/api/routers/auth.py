from fastapi import HTTPException, Depends, status, Request, APIRouter
from src.config.setting import Settings
import src.config.schemas as schemas
from src.api.dependencies import get_db
from sqlalchemy.orm import Session
from datetime import timedelta
from src.services.auth import create_access_token, authenticate_user


router = APIRouter(
    prefix="/token",
    tags=["token"]
)


@router.post("/")
async def login_for_access_token(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()
    email = form_data.get('email')
    password = form_data.get('password')
    user = authenticate_user(email, password, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=Settings().ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.fantasy_name}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")
