from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from models import Procedure, Staff, User


async def get_all_procedures_by_ids(
    procedure_ids: list[int], db: AsyncSession
) -> list[Procedure]:
    result = await db.execute(
        select(Procedure)
        .options(selectinload(Procedure.staff).selectinload(Staff.user))
        .where(Procedure.id.in_(procedure_ids))
    )
    return result.scalars().all()


async def get_all_staff_by_user_ids(
    user_ids: list[int], db: AsyncSession
) -> list[Staff]:
    result = await db.execute(select(Staff).where(Staff.user_id.in_(user_ids)))
    return result.scalars().all()
