from typing import Annotated

from fastapi import Depends, Query
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from constants.exceptions import AuthExceptions, UsersExceptions
from core.config import Settings, get_settings
from core.custom_logging import get_logger
from crud import users as users_crud
from db.session import get_db
from models import User
from security.tokens import TokenManager

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login', auto_error=False)
tokens = None
logger = get_logger(__name__)


def get_tokens(
    settings: Annotated[Settings, Depends(get_settings)],
) -> TokenManager:
    global tokens

    if not tokens:

        tokens = TokenManager(
            secret=settings.secret,
            algorithm=settings.algorithm,
        )

    return tokens


def depend_auth(
    token: Annotated[str, Depends(oauth2_scheme)],
    tokens: Annotated[TokenManager, Depends(get_tokens)],
) -> int:
    try:
        payload = tokens.decode(encode=token)
    except InvalidTokenError:
        raise AuthExceptions.credentials_exception

    user_id = payload.get('id')

    if not user_id:
        raise AuthExceptions.credentials_exception

    return user_id


async def depend_user_by_token(
    token: Annotated[str, Query()],
    tokens: Annotated[TokenManager, Depends(get_tokens)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    try:
        payload = tokens.decode(encode=token)
    except InvalidTokenError:
        raise AuthExceptions.credentials_exception

    user_id = payload.get('id')

    if not user_id:
        raise AuthExceptions.credentials_exception

    user = await users_crud.get_user_by_id(user_id, db)

    if not user:
        raise AuthExceptions.credentials_exception

    return user


async def depend_user_by_id(
    user_id: Annotated[int, Query()],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    user = await users_crud.get_user_by_id(user_id, db)

    if not user:
        raise UsersExceptions.user_not_found

    return user


async def depend_user(
    user_id: Annotated[int, Depends(depend_auth)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    user = await users_crud.get_user_by_id(user_id, db)

    if not user:
        raise AuthExceptions.credentials_exception

    return user
