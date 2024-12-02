from passlib.hash import pbkdf2_sha256
from .repositories import UserRepository
from .schemas import UserBase, UserUpdate
from fastapi import HTTPException
from .models import User


def verify_password(plain_password, hashed_password):
    return pbkdf2_sha256.verify(plain_password, hashed_password)


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def create_user(self, user_data: UserBase):
        hashed_password = pbkdf2_sha256.hash(user_data.password)
        user_data.password = hashed_password

        user_to_create = User(
            fantasy_name=user_data.fantasy_name,
            email=user_data.email,
            password=user_data.password,
            cnpj=user_data.cnpj
        )

        return self.user_repo.create(user_to_create)

    def update_user(self, user_id: int, user_data: UserUpdate):
        user = self.user_repo.get_by_id(user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user_data.email:

            existing_user = self.user_repo.get_by_email(user_data.email)

            if existing_user and existing_user.id != user_id:
                raise HTTPException(status_code=400, detail="Email already in use")

        for key, value in user_data.model_dump(exclude_unset=True).items():
            if key == "password":
                value = pbkdf2_sha256.hash(value)
            setattr(user, key, value)

        return self.user_repo.update(user)
