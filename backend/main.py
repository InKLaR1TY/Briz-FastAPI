from fastapi import FastAPI

from core.config import get_settings
from core.custom_logging import get_logger
from crud import users
from db.init_db import init_models
from db.session import async_session
from hooks.events import *
from routers import api
from schemas.users import SuperuserCreate

logger = get_logger(__name__)


async def lifespan(app: FastAPI):
    await init_models()
    async with async_session() as db:
        result = await users.create_superuser(
            SuperuserCreate(**get_settings().superuser_data), db
        )
        logger.info(result)
    logger.info('Работающие эндпоинты:')
    for route in app.router.routes:
        print(route.path, route.methods)
    yield


app = FastAPI(title=get_settings().title, lifespan=lifespan)
app.include_router(api)


@app.get('/')
async def main():
    return 'Запущено'


logger.info('Приложение запущено')
