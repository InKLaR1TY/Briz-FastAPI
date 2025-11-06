from fastapi import HTTPException, status
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from constants.enums import EntityName
from constants.exceptions import CatalogExceptions, UsersExceptions
from models import Category, Procedure, Staff
from schemas.catalog import (
    CategoryCreate,
    CategoryUpdate,
    ProcedureCreate,
    ProcedureUpdate,
)
from wrappers.handlers import db_exception_handler

from .general import get_all_staff_by_user_ids


@db_exception_handler(EntityName.category)
async def create_category(
    catagory_data: CategoryCreate, db: AsyncSession
) -> Category:
    category = Category(**catagory_data.model_dump(exclude_unset=True))
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category


@db_exception_handler(EntityName.category)
async def update_category(
    category_id: int, category_data: CategoryUpdate, db: AsyncSession
) -> Category:
    category = await get_category_by_id(category_id, db)
    if not category:
        raise CatalogExceptions.category_not_found

    for field, value in category_data.model_dump(exclude_unset=True).items():
        setattr(category, field, value)

    await db.commit()
    await db.refresh(category)
    return category


async def get_category_by_id(
    category_id: int, db: AsyncSession
) -> Category | None:
    result = await db.execute(
        select(Category)
        .options(
            selectinload(Category.procedures)
            .selectinload(Procedure.staff)
            .selectinload(Staff.user)
        )
        .where(Category.id == category_id)
    )
    return result.scalar_one_or_none()


async def get_all_categories(db: AsyncSession) -> list[Category]:
    result = await db.execute(
        select(Category).options(
            selectinload(Category.procedures)
            .selectinload(Procedure.staff)
            .selectinload(Staff.user)
        )
    )
    return result.scalars().all()


@db_exception_handler(EntityName.category)
async def delete_category(category_id: int, db: AsyncSession) -> None:
    result = await db.execute(
        select(Category).where(Category.id == category_id)
    )
    category = result.scalar_one_or_none()
    if not category:
        raise NoResultFound

    await db.delete(category)
    await db.commit()


@db_exception_handler(EntityName.procedure)
async def create_procedure(
    catagory_data: ProcedureCreate, db: AsyncSession
) -> Procedure:
    data = catagory_data.model_dump(exclude_unset=True)
    staff_ids = data.pop('staff_ids')
    staff = await get_all_staff_by_user_ids(staff_ids, db)
    procedure = Procedure(**data, staff=staff)
    db.add(procedure)
    await db.commit()
    await db.refresh(procedure)
    return procedure


@db_exception_handler(EntityName.procedure)
async def update_procedure(
    procedure_id: int, procedure_data: ProcedureUpdate, db: AsyncSession
) -> Procedure:
    async with db.begin():
        result = await db.execute(
            select(Procedure).where(Procedure.id == procedure_id)
        )
        procedure = result.scalar_one_or_none()
        if not procedure:
            raise CatalogExceptions.procedure_not_found

        data = procedure_data.model_dump(exclude_unset=True)
        staff_ids = data.pop('staff_ids', None)

        for field, value in data.items():
            setattr(procedure, field, value)

        if staff_ids is not None:
            staff_list = await get_all_staff_by_user_ids(staff_ids, db)

            if len(staff_list) != len(staff_ids):
                raise UsersExceptions.incorrect_id_masters

            procedure.staff = staff_list

    await db.refresh(procedure)
    return procedure


async def get_procedure_by_id(
    procedure_id: int, db: AsyncSession
) -> Procedure | None:
    result = await db.execute(
        select(Procedure)
        .options(selectinload(Procedure.staff).selectinload(Staff.user))
        .where(Procedure.id == procedure_id)
    )
    return result.scalar_one_or_none()


async def get_all_procedures(db: AsyncSession) -> list[Procedure]:
    result = await db.execute(
        select(Procedure).options(
            selectinload(Procedure.staff).selectinload(Staff.user)
        )
    )
    return result.scalars().all()


@db_exception_handler(EntityName.procedure)
async def delete_procedure(procedure_id: int, db: AsyncSession) -> None:
    result = await db.execute(
        select(Procedure).where(Procedure.id == procedure_id)
    )
    procedure = result.scalar_one_or_none()
    if not procedure:
        raise NoResultFound

    await db.delete(procedure)
    await db.commit()
