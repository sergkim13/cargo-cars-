import pytest
import pytest_asyncio
from cars_app.database.crud.location import LocationCRUD

from cars_app.validation.schemas import LocationCreate


@pytest.fixture
def location_data_1():
    return LocationCreate(
        city='Adjuntas',
        state='Puerto Rico',
        zip_code=601,
        latitude=18.18027,
        longtitude=-66.75266,
    )


@pytest.fixture
def location_data_2():
    return LocationCreate(
        city='Aguada',
        state='Puerto Rico',
        zip_code=602,
        latitude=18.36075,
        longtitude=-67.17541,
    )


@pytest.fixture
def location_data_3():
    return LocationCreate(
        city='Big Flats',
        state='New York',
        zip_code=14814,
        latitude=42.15525,
        longtitude=-76.95148,
    )


@pytest_asyncio.fixture
async def fixture_location_1(session, location_data_1):
    location_crud = LocationCRUD(session)
    return await location_crud.create(location_data_1)


@pytest_asyncio.fixture
async def fixture_location_2(session, location_data_2):
    location_crud = LocationCRUD(session)
    return await location_crud.create(location_data_2)


@pytest_asyncio.fixture
async def fixture_location_3(session, location_data_3):
    location_crud = LocationCRUD(session)
    return await location_crud.create(location_data_3)
