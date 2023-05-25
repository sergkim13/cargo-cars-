from http import HTTPStatus

import pytest

from cars_app.api.v1.routers.constants import (
    CARGO_LIST_FULL,
    CARGO_CREATE_FULL,
    CARGO_DETAIL_FULL,
    CARGO_UPDATE_FULL,
    CARGO_DELETE_FULL,
)
from cars_app.validation.schemas import (
    CargoCarsInfo,
    CargoInfo,
    CargoInfoDetail,
    CargoListElement,
)


@pytest.mark.asyncio
async def test_get_list_epmty(client):
    """Checks response of `cargo_list` endpoint with empty table."""
    response = await client.get(CARGO_LIST_FULL)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_list(client, fixture_cargo_1, fixture_cargo_2, fixture_cargo_3,
                        fixture_car_1, fixture_car_2, fixture_car_3):
    """Checks normal response of `cargo_list` endpoint."""
    response = await client.get(CARGO_LIST_FULL)
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 3
    assert CargoListElement.validate(response.json()[0])
    assert CargoListElement.validate(response.json()[1])
    assert CargoListElement.validate(response.json()[2])
    assert response.json()[0] == CargoListElement(
        id=fixture_cargo_1.id,
        pickup_location=fixture_cargo_1.pickup_location,
        delivery_location=fixture_cargo_1.delivery_location,
        nearby_cars_count=2,
        ).dict()
    assert response.json()[1] == CargoListElement(
        id=fixture_cargo_2.id,
        pickup_location=fixture_cargo_2.pickup_location,
        delivery_location=fixture_cargo_2.delivery_location,
        nearby_cars_count=2,
        ).dict()
    assert response.json()[2] == CargoListElement(
        id=fixture_cargo_3.id,
        pickup_location=fixture_cargo_3.pickup_location,
        delivery_location=fixture_cargo_3.delivery_location,
        nearby_cars_count=2,
        ).dict()


@pytest.mark.asyncio
async def test_get_detail(client, fixture_cargo_1, fixture_car_1, fixture_car_2, fixture_car_3):
    """Checks normal response of `cargo_detail` endpoint."""
    response = await client.get(CARGO_DETAIL_FULL.format(cargo_id=4))
    assert response.status_code == HTTPStatus.OK
    assert CargoInfoDetail.validate(response.json())
    assert response.json() == CargoInfoDetail(
        id=fixture_cargo_1.id,
        pickup_location=fixture_cargo_1.pickup_location,
        delivery_location=fixture_cargo_1.delivery_location,
        weight=fixture_cargo_1.weight,
        description=fixture_cargo_1.description,
        cars_info=[
            CargoCarsInfo(
                number_plate=fixture_car_1.number_plate,
                distance_to_cargo=0.0,
            ),
            CargoCarsInfo(
                number_plate=fixture_car_2.number_plate,
                distance_to_cargo=30.42,
            ),
            CargoCarsInfo(
                number_plate=fixture_car_3.number_plate,
                distance_to_cargo=1757.56,
            ),
        ]
    ).dict()


@pytest.mark.asyncio
async def test_create(client, cargo_data_1, fixture_location_1, fixture_location_2):
    """Checks normal response of `cargo_create` endpoint."""
    response = await client.post(CARGO_CREATE_FULL, json=cargo_data_1.dict())
    assert response.status_code == HTTPStatus.CREATED
    assert CargoInfo.validate(response.json())
    assert response.json()['id']
    assert response.json()['pickup_location'] == cargo_data_1.pickup_location
    assert response.json()['delivery_location'] == cargo_data_1.delivery_location
    assert response.json()['weight'] == cargo_data_1.weight
    assert response.json()['description'] == cargo_data_1.description


@pytest.mark.asyncio
async def test_update(client, fixture_cargo_1, cargo_update_data):
    """Checks normal response of `cargo_update` endpoint."""
    response = await client.patch(CARGO_UPDATE_FULL.format(
        cargo_id=fixture_cargo_1.id), json=cargo_update_data.dict()
    )
    assert response.status_code == HTTPStatus.OK
    assert CargoInfo.validate(response.json())
    assert response.json() == CargoInfo(
        id=fixture_cargo_1.id,
        pickup_location=fixture_cargo_1.pickup_location,
        delivery_location=fixture_cargo_1.delivery_location,
        weight=cargo_update_data.weight,
        description=cargo_update_data.description,
    )


@pytest.mark.asyncio
async def test_delete(client, fixture_cargo_1):
    """Checks normal response of `cargo_delete` endpoint."""
    response = await client.delete(CARGO_DELETE_FULL.format(cargo_id=fixture_cargo_1.id))
    check_existance = await client.get(CARGO_DETAIL_FULL.format(cargo_id=fixture_cargo_1.id))
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert check_existance.status_code == HTTPStatus.NOT_FOUND
