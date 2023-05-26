import asyncio

from fastapi import FastAPI

from cars_app.api.v1.routers.car import router as car_router
from cars_app.api.v1.routers.cargo import router as cargo_router
from cars_app.database.settings import async_session
from cars_app.services.helper import get_helper_service
from config import INTERVAL_SECONDS

app = FastAPI(
    title='Cars API',
    description='Cars API, powered by FastAPI',
    version='1.0.0',
    docs_url='/docs',
    redoc_url='/redoc',
)
app.include_router(cargo_router)
app.include_router(car_router)


async def populate_db():
    async with async_session() as session:
        helper_service = get_helper_service(session)
        await helper_service.populate_locations()
        await helper_service.populate_cars()


async def update_cars_locations_random():
    while True:
        await asyncio.sleep(INTERVAL_SECONDS)
        async with async_session() as session:
            helper_service = get_helper_service(session)
            await helper_service.update_locations_random()


@app.on_event('startup')
async def startup_event():
    loop = asyncio.get_event_loop()
    await populate_db()
    loop.create_task(update_cars_locations_random())
