import pytest
import pytest_asyncio

from cars_app.database.crud.cargo import CargoCRUD
from cars_app.validation.schemas import CargoCreate, CargoUpdate


@pytest.fixture
def cargo_data_1(location_data_1, location_data_2):
    return CargoCreate(
        pickup_location=location_data_1.zip_code,
        delivery_location=location_data_2.zip_code,
        weight=500,
        description='description 1',
    )


@pytest.fixture
def cargo_data_2(location_data_1, location_data_3):
    return CargoCreate(
        pickup_location=location_data_1.zip_code,
        delivery_location=location_data_3.zip_code,
        weight=700,
        description='description 2',
    )


@pytest.fixture
def cargo_data_3(location_data_2, location_data_3):
    return CargoCreate(
        pickup_location=location_data_2.zip_code,
        delivery_location=location_data_3.zip_code,
        weight=300,
        description='description 3',
    )


@pytest_asyncio.fixture
async def fixture_cargo_1(session, cargo_data_1, fixture_location_1, fixture_location_2):
    cargo_crud = CargoCRUD(session)
    return await cargo_crud.create(cargo_data_1)


@pytest_asyncio.fixture
async def fixture_cargo_2(session, cargo_data_2, fixture_location_1, fixture_location_3):
    cargo_crud = CargoCRUD(session)
    return await cargo_crud.create(cargo_data_2)


@pytest_asyncio.fixture
async def fixture_cargo_3(session, cargo_data_3, fixture_location_2, fixture_location_3):
    cargo_crud = CargoCRUD(session)
    return await cargo_crud.create(cargo_data_3)


@pytest.fixture
def cargo_update_data():
    return CargoUpdate(weight=100, description='Updated description.')
