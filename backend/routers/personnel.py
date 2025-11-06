from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from constants.return_messages import PersonnelMessages
from core.custom_logging import get_logger
from crud import personnel as personnel_crud
from db.session import get_db
from depends.permissions import Permissions
from schemas.personnel import WorkDaysBulkUpdate

logger = get_logger(__name__)

personnel_router = APIRouter(prefix='/personnel')


@personnel_router.post(
    '/work-dates',
    dependencies=[Depends(Permissions.is_admin_or_owner_permission)],
)
async def update_work_days(
    data: WorkDaysBulkUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    await personnel_crud.update_work_days_bulk(data, db)
    return {'detail': PersonnelMessages.updated_work_dates}
