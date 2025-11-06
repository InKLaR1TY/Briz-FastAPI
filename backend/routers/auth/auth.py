from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from constants.exceptions import AuthExceptions, UsersExceptions
from core.custom_logging import get_logger
from crud import users as users_crud
from db.session import get_db
from depends.permissions import Permissions
from depends.tokens import get_tokens
from schemas.auth import DecodedToken, TokenResponse, UserLogin
from security.passwords import PasswordManager
from security.tokens import TokenManager

logger = get_logger(__name__)

auth_router = APIRouter(prefix='/auth')


@auth_router.post(
    '/login',
    response_model=TokenResponse,
    dependencies=[Depends(Permissions.not_authenticated_permission)],
)
async def login(
    data: UserLogin,
    tokens: Annotated[TokenManager, Depends(get_tokens)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    user = await users_crud.get_user_by_phone_number(data.phone_number, db)

    if not user:
        raise UsersExceptions.user_not_found

    verify = PasswordManager().verify_password(data.password, user.password)
    if not verify:
        raise AuthExceptions.credentials_exception
    decoded_token = DecodedToken(_id=str(user.id))
    token = tokens.generate(decoded_token)
    return TokenResponse(token=token)
