from fastapi import FastAPI

from cars_app.api.v1.routers.car import router as car_router
from cars_app.api.v1.routers.cargo import router as cargo_router
from cars_app.database.settings import async_session
from cars_app.services.helper import get_helper_service

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


@app.on_event('startup')
async def startup_event():
    await populate_db()
