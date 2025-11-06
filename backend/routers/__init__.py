from fastapi import APIRouter

from .auth.auth import auth_router
from .catalog.categories import categories_router
from .catalog.procedures import procedures_router
from .users.staff import staff_router
from .users.users import users_router

api = APIRouter(prefix='/api')
api.include_router(auth_router)
api.include_router(users_router)
api.include_router(staff_router)
api.include_router(procedures_router)
api.include_router(categories_router)
