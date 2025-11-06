from typing import Annotated

from fastapi import Depends

from constants.exceptions import AuthExceptions
from core.custom_logging import get_logger
from models import User

from .tokens import depend_user, depend_user_by_id, oauth2_scheme

logger = get_logger(__name__)


class Permissions:
    is_superuser = 'superuser'
    is_staff = 'staff'
    is_admin = 'admin'
    is_master = 'master'
    is_owner = 'owner'
    is_authenticated = 'authenticated'

    @staticmethod
    async def is_superuser_permission(
        user: Annotated[User, Depends(depend_user)],
    ) -> User:
        """Только для суперпользователя"""
        if not user.is_superuser:
            raise AuthExceptions.forbidden
        return user

    @staticmethod
    async def is_staff_permission(
        user: Annotated[User, Depends(depend_user)],
    ) -> User:
        """Только для сотрудников (мастеров, админов)"""
        if not user.is_staff:
            raise AuthExceptions.forbidden
        return user

    @staticmethod
    async def is_owner_permission(
        user: Annotated[User, Depends(depend_user)],
    ) -> User:
        """Только для владельца"""
        if not user.staff:
            raise AuthExceptions.forbidden
        return user

    @staticmethod
    async def is_admin_permission(
        user: Annotated[User, Depends(depend_user)],
    ) -> User:
        """Только для админов"""
        if not user.staff.is_admin:
            raise AuthExceptions.forbidden
        return user

    @staticmethod
    async def is_master_permission(
        user: Annotated[User, Depends(depend_user)],
    ) -> User:
        """Только для мастеров"""
        if not user.staff.is_admin:
            raise AuthExceptions.forbidden
        return user

    @staticmethod
    async def is_self_permission(
        user: Annotated[User, Depends(depend_user)],
        requested_user: Annotated[User, Depends(depend_user_by_id)],
    ) -> User:
        """Только сам пользователь"""
        if user.id != requested_user.id:
            raise AuthExceptions.forbidden
        return requested_user

    @staticmethod
    async def not_authenticated_permission(
        token: Annotated[str, Depends(oauth2_scheme)] = None,
    ):
        """Только для незалогиненных пользователей"""
        if token:
            raise AuthExceptions.forbidden
        return None

    @staticmethod
    async def authenticated_permission(
        user: Annotated[User, Depends(depend_user)],
    ) -> User:
        """Только для залогиненных пользователей"""
        return user

    @staticmethod
    async def is_admin_or_owner_permission(
        user: Annotated[User, Depends(depend_user)],
    ) -> User:
        """Только админам или владельцам"""
        try:
            return await Permissions.is_superuser_permission(user)
        except AuthExceptions.forbidden:
            pass

        try:
            return await Permissions.is_admin_permission(user)
        except AuthExceptions.forbidden:
            pass

        try:
            return await Permissions.is_owner_permission(user)
        except AuthExceptions.forbidden:
            pass

        raise AuthExceptions.forbidden

    @staticmethod
    def get_user_permissions(user: User):
        """Генератор разрешений для fastapi-permissions"""
        if user.is_superuser:
            yield Permissions.is_superuser
        if user.is_staff:
            yield Permissions.is_staff
        if user.staff.is_admin:
            yield Permissions.is_admin
        if user.staff.is_master:
            yield Permissions.is_master
        if user.staff.is_owner:
            yield Permissions.is_owner
        yield Permissions.is_authenticated
