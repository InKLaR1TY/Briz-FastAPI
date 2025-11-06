from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from constants.return_messages import CatalogMessages
from core.custom_logging import get_logger
from crud import catalog as catalog_crud
from db.session import get_db
from depends.permissions import Permissions
from schemas.catalog import (
    ProcedureCreate,
    ProcedureRead,
    ProcedureShortRead,
    ProcedureUpdate,
)

logger = get_logger(__name__)

procedures_router = APIRouter(prefix='/procedures')


@procedures_router.post(
    '/',
    response_model=ProcedureRead,
    dependencies=[Depends(Permissions.is_admin_or_owner_permission)],
)
async def create_procedure(
    procedure_data: ProcedureCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await catalog_crud.create_procedure(procedure_data, db)


@procedures_router.patch(
    '/{procedure_id}',
    response_model=ProcedureRead,
    dependencies=[Depends(Permissions.is_admin_or_owner_permission)],
)
async def update_procedure(
    procedure_id: int,
    procedure_data: ProcedureUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await catalog_crud.update_procedure(
        procedure_id, procedure_data, db
    )


@procedures_router.get('/', response_model=list[ProcedureShortRead])
async def get_all_procedures(db: Annotated[AsyncSession, Depends(get_db)]):
    return await catalog_crud.get_all_procedures(db)


@procedures_router.get('/{procedure_id}', response_model=ProcedureRead)
async def get_procedure(
    procedure_id: int, db: Annotated[AsyncSession, Depends(get_db)]
):
    return await catalog_crud.get_procedure_by_id(procedure_id, db)


@procedures_router.delete(
    '/{procedure_id}',
    dependencies=[Depends(Permissions.is_admin_or_owner_permission)],
)
async def delete_procedure(
    procedure_id: int, db: Annotated[AsyncSession, Depends(get_db)]
):
    await catalog_crud.delete_procedure(procedure_id, db)
    return {'detail': CatalogMessages.deleted_procedure}


logger.info('procedures_router файл загружен')
