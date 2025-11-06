from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from constants.return_messages import CatalogMessages
from core.custom_logging import get_logger
from crud import catalog as catalog_crud
from db.session import get_db
from depends.permissions import Permissions
from schemas.catalog import (
    CategoryCreate,
    CategoryRead,
    CategoryShortRead,
    CategoryUpdate,
)

logger = get_logger(__name__)

categories_router = APIRouter(prefix='/categories')


@categories_router.post(
    '/',
    response_model=CategoryRead,
    dependencies=[Depends(Permissions.is_admin_or_owner_permission)],
)
async def create_category(
    category_data: CategoryCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await catalog_crud.create_category(category_data, db)


@categories_router.patch(
    '/{category_id}',
    response_model=CategoryRead,
    dependencies=[Depends(Permissions.is_admin_or_owner_permission)],
)
async def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await catalog_crud.update_category(category_id, category_data, db)


@categories_router.get('/', response_model=list[CategoryShortRead])
async def get_all_categories(db: Annotated[AsyncSession, Depends(get_db)]):
    return await catalog_crud.get_all_categories(db)


@categories_router.get('/{category_id}', response_model=CategoryRead)
async def get_category(
    category_id: int, db: Annotated[AsyncSession, Depends(get_db)]
):
    return await catalog_crud.get_category_by_id(category_id, db)


@categories_router.delete(
    '/{category_id}',
    dependencies=[Depends(Permissions.is_admin_or_owner_permission)],
)
async def delete_category(
    category_id: int, db: Annotated[AsyncSession, Depends(get_db)]
):
    await catalog_crud.delete_category(category_id, db)
    return {'detail': CatalogMessages.deleted_category}


logger.info('categories_router файл загружен')
