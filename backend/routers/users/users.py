from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from constants.return_messages import UsersMessages
from core.custom_logging import get_logger
from crud import users as users_crud
from db.session import get_db
from depends.permissions import Permissions
from depends.tokens import depend_user
from models import User
from schemas.users import (
    UserCreate,
    UserRead,
    UserUpdate,
    UserUpdatePassword,
    UserUpdatePhoneNumber,
)

logger = get_logger(__name__)

users_router = APIRouter(prefix='/users')


@users_router.get(
    '/me',
    response_model=UserRead,
)
async def get_me(user: Annotated[User, Depends(depend_user)]):
    return user


@users_router.patch(
    '/me',
    response_model=UserRead,
)
async def update_me(
    user_data: UserUpdate,
    user: Annotated[User, Depends(depend_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await users_crud.update_user(user.id, user_data, db)


@users_router.post(
    '/',
    response_model=UserRead,
    dependencies=[Depends(Permissions.is_admin_or_owner_permission)],
)
async def create_user(
    user_data: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]
):
    return await users_crud.create_user(user_data, db)


@users_router.patch(
    '/{user_id}',
    response_model=UserRead,
    dependencies=[Depends(Permissions.is_admin_or_owner_permission)],
)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await users_crud.update_user(user_id, user_data, db)


@users_router.patch(
    '/{user_id}/change-phone-number',
    response_model=UserRead,
    dependencies=[Depends(Permissions.is_admin_or_owner_permission)],
)
async def update_phone_number_user(
    user_id: int,
    user_data: UserUpdatePhoneNumber,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await users_crud.update_user(
        user_id, UserUpdate(phone_number=user_data.phone_number), db
    )


@users_router.patch(
    '/{user_id}/change-password',
    dependencies=[Depends(Permissions.is_admin_or_owner_permission)],
)
async def update_password_user(
    user_id: int,
    user_data: UserUpdatePassword,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    await users_crud.update_password_user(user_id, user_data, db)
    return {'detail': UsersMessages.change_password}


@users_router.get('/', response_model=list[UserRead])
async def get_all_users(db: Annotated[AsyncSession, Depends(get_db)]):
    return await users_crud.get_all_users(db)


@users_router.get('/{user_id}', response_model=UserRead)
async def get_user(user_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    return await users_crud.get_user_by_id(user_id, db)


logger.info('users_router файл загружен')
