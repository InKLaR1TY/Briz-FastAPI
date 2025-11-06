from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from constants.return_messages import PersonnelMessages
from core.custom_logging import get_logger
from crud import users as users_crud
from db.session import get_db
from depends.permissions import Permissions
from depends.tokens import depend_user
from models import User
from schemas.users import (
    StaffUserUpdate,
    StaffWorkDaysUpdate,
    UserCreate,
    UserRead,
)

logger = get_logger(__name__)

staff_router = APIRouter(prefix='/staff')


@staff_router.patch(
    '/me',
    response_model=UserRead,
)
async def update_me(
    user_data: StaffUserUpdate,
    user: Annotated[User, Depends(depend_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await users_crud.update_staff(user.id, user_data, db)


@staff_router.post(
    '/',
    response_model=UserRead,
    dependencies=[Depends(Permissions.is_admin_or_owner_permission)],
)
async def create_staff(
    staff_data: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]
):
    return await users_crud.create_staff(staff_data, db)


@staff_router.patch('/{user_id}', response_model=UserRead)
async def update_staff_work_days(
    user_id: int,
    data: StaffWorkDaysUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    await users_crud.update_staff_work_days(data, db)
    return {'detail': PersonnelMessages.updated_work_dates}


@staff_router.patch('/{user_id}', response_model=UserRead)
async def update_staff(
    user_id: int,
    staff_data: StaffUserUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await users_crud.update_staff(user_id, staff_data, db)


@staff_router.get('/', response_model=list[UserRead])
async def get_all_staff(db: Annotated[AsyncSession, Depends(get_db)]):
    return await users_crud.get_all_staff(db)


# @staff_router.get('/{user_id}', response_model=UserRead)
# async def get_staff(user_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
#     return await users_crud.get_user_by_id(user_id, db)


logger.info('staff_router файл загружен')
