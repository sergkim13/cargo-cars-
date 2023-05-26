from http import HTTPStatus

import pytest

from cars_app.api.v1.routers.constants import CAR_UPDATE_FULL
from cars_app.validation.schemas import CarInfo


@pytest.mark.asyncio
async def test_update(client, fixture_car_1, fixture_location_3, car_update_data):
    """Checks normal response of `car_update` endpoint."""
    response = await client.patch(CAR_UPDATE_FULL.format(
        car_id=fixture_car_1.id), json=car_update_data.dict()
    )
    assert response.status_code == HTTPStatus.OK
    assert CarInfo.validate(response.json())
    assert response.json()['current_location'] == car_update_data.current_location
    # assert response.json() == CarInfo(
    #     id=fixture_car_1.id,
    #     capacity=fixture_car_1.capacity,
    #     number_plate=fixture_car_1.number_plate,
    #     current_location=car_update_data.current_location,
    # ).dict()
