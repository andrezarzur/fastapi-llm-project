from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.api.dependencies import get_db
from src.domains.users.schemas import UserBase, UserUpdate
from src.decorators.exception import handle_exceptions
from src.domains.users.repositories import UserRepository
from src.domains.users.services import UserService
from src.api.dependencies import validate_token_dependency


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get('/')
@handle_exceptions
def get_users(db: Session = Depends(get_db), _: None = Depends(validate_token_dependency)):
    user_repo = UserRepository(db)
    return user_repo.get_all()


@router.get('/{user_id}')
@handle_exceptions
def get_user(user_id: int, db: Session = Depends(get_db), _: None = Depends(validate_token_dependency)):
    user_repo = UserRepository(db)
    return user_repo.get_by_id(user_id)


@router.post('/')
@handle_exceptions
def create_user(user: UserBase, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)
    return user_service.create_user(user)


@router.put('/{user_id}')
@handle_exceptions
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db), _: None = Depends(validate_token_dependency)):
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)
    return user_service.update_user(user_id, user_update)


@router.delete('/{user_id}')
@handle_exceptions
def delete_user(user_id: int, db: Session = Depends(get_db), _: None = Depends(validate_token_dependency)):
    user_repo = UserRepository(db)
    return user_repo.delete(user_id)
