from sqlalchemy import delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from constants.enums import EntityName
from constants.exceptions import CatalogExceptions, UsersExceptions
from constants.return_messages import UsersMessages
from core.custom_logging import get_logger
from models import Staff, User, WorkDay
from schemas.users import (
    StaffUserUpdate,
    StaffWorkDaysUpdate,
    SuperuserCreate,
    UserCreate,
    UserUpdate,
    UserUpdatePassword,
)
from security.passwords import PasswordManager
from wrappers.handlers import db_exception_handler

from .general import get_all_procedures_by_ids

logger = get_logger(__name__)


@db_exception_handler(EntityName.staff)
async def create_staff(user_data: UserCreate, db: AsyncSession) -> User:
    data = user_data.model_dump(exclude_unset=True)
    staff_data: dict = data.pop('staff', {})
    procedure_ids = staff_data.pop('procedure_ids')

    async with db.begin():
        user = await create_user(UserCreate(**data), db, False)
        db.add(user)
        await db.flush()

        procedures = await get_all_procedures_by_ids(procedure_ids, db)
        staff = Staff(**staff_data, user_id=user.id, procedures=procedures)
        db.add(staff)

    await db.refresh(user)
    return user


@db_exception_handler(EntityName.staff)
async def update_staff(
    user_id: int, staff_data: StaffUserUpdate, db: AsyncSession
):
    async with db.begin():

        logger.debug(staff_data)
        user = await get_user_by_id(user_id, db)
        if not user:
            raise NoResultFound
        staff = user.staff

        user_data = staff_data.model_dump(exclude_unset=True)
        data: dict = user_data.pop('staff', {})
        procedure_ids = data.pop('procedure_ids', None)

        updated_user = await update_user(
            user_id, UserUpdate(**user_data), db, False
        )

        for field, value in data.items():
            setattr(staff, field, value)

        if procedure_ids is not None:
            procedures_list = await get_all_procedures_by_ids(
                procedure_ids, db
            )

            if len(procedures_list) != len(procedure_ids):
                raise CatalogExceptions.incorrect_id_procedures

            staff.procedures = procedures_list

    await db.commit()
    await db.refresh(user)
    await db.refresh(staff)
    return updated_user


async def update_staff_work_days(
    data: StaffWorkDaysUpdate, db: AsyncSession, commit: bool = True
):
    try:
        staff_id = data.staff_id

        objects_to_add = [
            WorkDay(staff_id=staff_id, work_date=work_date)
            for work_date in (data.add_dates or [])
        ]

        if data.remove_dates:
            await db.execute(
                delete(WorkDay).where(
                    WorkDay.staff_id == staff_id,
                    WorkDay.work_date.in_(data.remove_dates),
                )
            )

        if objects_to_add:
            db.add_all(objects_to_add)

        if commit:
            await db.commit()

    except Exception:
        await db.rollback()
        raise


async def get_all_staff(db: AsyncSession) -> list[User]:
    result = await db.execute(select(User).where(User.is_staff))
    return result.scalars().all()


@db_exception_handler(EntityName.user)
async def create_user(
    user_data: UserCreate, db: AsyncSession, commit: bool = True
) -> User:
    data = user_data.model_dump(exclude_unset=True)
    password = PasswordManager().hash_password(data.pop('password'))
    user = User(**data, password=password)
    db.add(user)
    if commit:
        await db.commit()
    await db.refresh(user)

    return user


@db_exception_handler(EntityName.user)
async def update_user(
    user_id: int, user_data: UserUpdate, db: AsyncSession, commit: bool = True
) -> User:
    user = await get_user_by_id(user_id, db)
    if not user:
        raise NoResultFound

    for field, value in user_data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)

    if commit:
        await db.commit()
    await db.refresh(user)
    return user


async def update_password_user(
    user_id: int,
    user_data: UserUpdatePassword,
    db: AsyncSession,
    commit: bool = True,
) -> None:
    user = await get_user_by_id(user_id, db)
    password = PasswordManager().hash_password(user_data.password)
    setattr(user, 'password', password)

    if commit:
        await db.commit()
    await db.refresh(user)


async def get_user_by_id(user_id: int, db: AsyncSession) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_username(username: str, db: AsyncSession) -> User | None:
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def get_user_by_phone_number(
    phone_number: str, db: AsyncSession
) -> User | None:
    result = await db.execute(
        select(User).where(User.phone_number == phone_number)
    )
    return result.scalar_one_or_none()


async def get_all_users(db: AsyncSession) -> list[User]:
    result = await db.execute(select(User))
    return result.scalars().all()


async def create_superuser(
    superuser_data: SuperuserCreate, db: AsyncSession
) -> str:
    data = superuser_data.model_dump(exclude_unset=True)
    user = await get_user_by_phone_number(data.get('phone_number'), db)
    if not user:
        password = PasswordManager().hash_password(data.pop('password'))
        superuser = User(**data, password=password, is_superuser=True)
        db.add(superuser)
        await db.commit()
        await db.refresh(superuser)
        return UsersMessages.created_superuser
    else:
        return UsersMessages.exists_superuser
