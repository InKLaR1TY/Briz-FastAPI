from sqlalchemy import ForeignKey, Integer, String, func, select
from sqlalchemy.orm import Mapped, column_property, mapped_column, relationship

from db.base import Base

from .associations import staff_procedures_table


class Procedure(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(70), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(
        String(300), unique=False, nullable=True
    )
    price: Mapped[int] = mapped_column(
        Integer,
        unique=False,
        nullable=False,
    )
    staff: Mapped[list['Staff']] = relationship(
        secondary=staff_procedures_table,
        back_populates='procedures',
        lazy='selectin',
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey('category.id'), nullable=False
    )
    category: Mapped['Category'] = relationship(
        back_populates='procedures', lazy='selectin'
    )


class Category(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(70), unique=True, nullable=False)
    procedures: Mapped[list['Procedure']] = relationship(
        back_populates='category',
        lazy='selectin',
        cascade='all, delete-orphan',
    )
    services_count: Mapped[int] = column_property(
        select(func.count(Procedure.id))
        .where(Procedure.category_id == id)
        .correlate_except(Procedure)
        .scalar_subquery()
    )
