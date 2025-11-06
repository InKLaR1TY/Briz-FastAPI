from datetime import date
from typing import List, Optional

from pydantic import BaseModel, field_validator, model_validator

from validators.users_validators import (
    validate_phone_number,
    validate_staff_required,
)


class UserBase(BaseModel):
    phone_number: str
    first_name: str
    last_name: str
    surname: Optional[str] = None
    is_staff: bool


class UserCreate(UserBase):
    staff: Optional['StaffCreate'] = None
    password: str
    _validate_phone_number = field_validator('phone_number')(
        validate_phone_number
    )

    @model_validator(mode='after')
    def check_staff(cls, values):
        return validate_staff_required(values)


class UserUpdate(BaseModel):
    phone_number: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    surname: Optional[str] = None


class UserUpdatePhoneNumber(BaseModel):
    phone_number: str


class UserUpdatePassword(BaseModel):
    password: str


class UserRead(UserBase):
    id: int
    username: str
    staff: Optional['StaffRead'] = None

    model_config = {'from_attributes': True}


class UserShortRead(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    surname: Optional[str] = None


class StaffBase(BaseModel):
    is_master: bool
    is_admin: bool
    is_fired: bool
    is_owner: bool


class StaffCreate(StaffBase):
    procedure_ids: List[int] = []


class StaffUpdate(BaseModel):
    is_master: Optional[bool] = None
    is_admin: Optional[bool] = None
    is_fired: Optional[bool] = None
    is_owner: Optional[bool] = None
    procedure_ids: Optional[List[int]] = None


class StaffUserUpdate(UserUpdate):
    staff: StaffUpdate


class StaffWorkDaysUpdate(BaseModel):
    staff_id: int
    add_dates: List[date] = []
    remove_dates: List[date] = []


class StaffRead(StaffBase):
    id: int
    procedures: List['ProcedureShortRead'] = []
    work_days: List['WorkDaysShortRead'] = []

    model_config = {'from_attributes': True}


class StaffUserShortRead(BaseModel):
    user: UserShortRead


class SuperuserCreate(BaseModel):
    phone_number: str
    first_name: str
    last_name: str
    password: str


from .catalog import ProcedureShortRead
from .personnel import WorkDaysShortRead

UserRead.model_rebuild()
StaffRead.model_rebuild()
