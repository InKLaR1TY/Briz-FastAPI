from typing import Optional

from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base

from .associations import staff_procedures_table


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    phone_number: Mapped[str] = mapped_column(
        String, unique=True, nullable=False
    )
    username: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False
    )
    first_name: Mapped[str] = mapped_column(
        String(100), unique=False, nullable=False
    )
    last_name: Mapped[str] = mapped_column(
        String(100), unique=False, nullable=False
    )
    surname: Mapped[str] = mapped_column(
        String(100), unique=False, nullable=True
    )
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    is_staff: Mapped[bool] = mapped_column(
        Boolean, unique=False, default=False
    )
    staff: Mapped[Optional['Staff']] = relationship(
        back_populates='user', lazy='selectin'
    )
    password: Mapped[str] = mapped_column(String, nullable=False)

    @property
    def get_fullname(self):
        fullname = self.last_name + self.first_name
        if self.surname is not None:
            fullname += self.surname
        return fullname


class Staff(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='staff')
    is_master: Mapped[bool] = mapped_column(Boolean, default=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_owner: Mapped[bool] = mapped_column(Boolean, default=False)
    is_fired: Mapped[bool] = mapped_column(Boolean, default=False)
    work_days: Mapped[list['WorkDay']] = relationship(
        'WorkDay', back_populates='staff', cascade='all, delete-orphan'
    )
    procedures: Mapped[list['Procedure']] = relationship(
        secondary=staff_procedures_table,
        back_populates='staff',
        lazy='selectin',
    )
