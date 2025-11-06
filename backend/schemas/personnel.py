from datetime import date
from typing import List

from pydantic import BaseModel

from .users import StaffWorkDaysUpdate


class WorkDaysRead(BaseModel):
    id: int
    staff_id: int
    work_dates: List[date]


class WorkDaysCalendarRead(BaseModel):
    staff_dates: List[WorkDaysRead]


class WorkDaysShortRead(BaseModel):
    id: int
    work_dates: List[date]


class WorkDaysBulkUpdate(BaseModel):
    staff_days: List[StaffWorkDaysUpdate]
