from typing import List, Optional

from pydantic import BaseModel, field_validator


class CategoryBase(BaseModel):
    title: str


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    title: Optional[str] = None


class CategoryRead(CategoryBase):
    id: int
    slug: str
    procedures: List['ProcedureShortRead'] = []
    services_count: int

    model_config = {'from_attributes': True}


class CategoryShortRead(BaseModel):
    id: int
    title: str
    slug: str
    services_count: int


class ProcedureBase(BaseModel):
    title: str
    description: str
    price: int


class ProcedureCreate(ProcedureBase):
    staff_ids: List[int] = []
    category_id: int


class ProcedureUpdate(BaseModel):
    staff_ids: Optional[List[int]] = None
    title: Optional[str] = None
    price: Optional[int] = None
    description: Optional[str] = None
    category_id: Optional[int] = None


class ProcedureRead(ProcedureBase):
    id: int
    category: CategoryShortRead
    staff: List['StaffUserShortRead'] = []

    model_config = {'from_attributes': True}


class ProcedureShortRead(BaseModel):
    id: int
    title: str
    slug: str
    price: int
    category: CategoryShortRead


from .users import StaffUserShortRead

CategoryRead.model_rebuild()
ProcedureRead.model_rebuild()
