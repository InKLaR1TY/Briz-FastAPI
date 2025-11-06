from sqlalchemy.ext.asyncio import AsyncSession

from schemas.personnel import WorkDaysBulkUpdate

from .users import update_staff_work_days


async def update_work_days_bulk(data: WorkDaysBulkUpdate, db: AsyncSession):
    for staff_days in data.staff_days:
        await update_staff_work_days(staff_days, db, False)

    await db.commit()
