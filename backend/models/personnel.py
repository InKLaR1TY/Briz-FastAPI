from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


class WorkDay(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    staff_id: Mapped[int] = mapped_column(
        ForeignKey('staff.id'), nullable=True
    )
    work_date: Mapped[Date] = mapped_column(Date)

    staff: Mapped['Staff'] = relationship(
        back_populates='work_days',
        lazy='selectin',
    )
