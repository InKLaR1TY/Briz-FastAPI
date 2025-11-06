from functools import wraps

from sqlalchemy.exc import IntegrityError, NoResultFound

from constants.enums import EntityName
from constants.exceptions import DBExceptions


def db_exception_handler(entity_key: EntityName):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except IntegrityError:
                raise DBExceptions.conflict(entity_key.value)
            except NoResultFound:
                raise DBExceptions.not_found(entity_key.value)

        return wrapper

    return decorator
