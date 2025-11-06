import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from core.config import get_settings
from db.base import Base


def default_expired():
    return (
        (
            datetime.datetime.now()
            + datetime.timedelta(minutes=get_settings().default_expire_minutes)
        )
        .timestamp()
        .__int__()
    )


class DecodedToken(BaseModel):
    id: int = Field(alias="_id")
    expired: datetime.datetime = Field(
        default_factory=default_expired,
        alias="exp",
    )

    model_config = ConfigDict(arbitrary_types_allowed=True)


class TokenResponse(BaseModel):
    token: str
    type: str = 'bearer'


class UserLogin(BaseModel):
    phone_number: str
    password: str
