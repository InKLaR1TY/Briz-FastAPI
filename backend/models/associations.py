from sqlalchemy import Column, ForeignKey, Table

from db.base import Base

staff_procedures_table = Table(
    'staff_procedures',
    Base.metadata,
    Column('staff_id', ForeignKey('staff.id'), primary_key=True),
    Column('procedures_id', ForeignKey('procedure.id'), primary_key=True),
)
