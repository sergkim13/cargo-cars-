import pytest
import pytest_asyncio

from cars_app.database.crud.car import CarCRUD
from cars_app.validation.schemas import CarCreate, CarUpdate


@pytest.fixture
def car_data_1(location_data_1):
    return CarCreate(
        number_plate='1111A',
        current_location=location_data_1.zip_code,
        capacity=600,
    )


@pytest.fixture
def car_data_2(location_data_2):
    return CarCreate(
        number_plate='2222B',
        current_location=location_data_2.zip_code,
        capacity=700,
    )


@pytest.fixture
def car_data_3(location_data_3):
    return CarCreate(
        number_plate='3333C',
        current_location=location_data_3.zip_code,
        capacity=1000,
    )


@pytest_asyncio.fixture
async def fixture_car_1(session, car_data_1, fixture_location_1):
    car_crud = CarCRUD(session)
    return await car_crud.create(car_data_1)


@pytest_asyncio.fixture
async def fixture_car_2(session, car_data_2, fixture_location_2):
    car_crud = CarCRUD(session)
    return await car_crud.create(car_data_2)


@pytest_asyncio.fixture
async def fixture_car_3(session, car_data_3, fixture_location_3):
    car_crud = CarCRUD(session)
    return await car_crud.create(car_data_3)


@pytest.fixture
def car_update_data(location_data_3):
    return CarUpdate(current_location=location_data_3.zip_code)
