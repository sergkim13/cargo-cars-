from http import HTTPStatus

from fastapi import APIRouter, Depends

from cars_app.api.v1.routers.constants import CAR_PREFIX, CAR_UPDATE
from cars_app.services.car import CarService, get_car_service
from cars_app.validation.schemas import CarInfo, CarUpdate

router = APIRouter(
    prefix=CAR_PREFIX,
    tags=['car'],
)


@router.patch(
    path=CAR_UPDATE,
    status_code=HTTPStatus.OK,
    response_model=CarInfo,
    summary='Редактирование информации о машине',
)
async def car_update(
    car_id: int,
    data: CarUpdate,
    car_service: CarService = Depends(get_car_service),
) -> CarInfo:
    """Update specific car."""
    return await car_service.update(car_id, data)
