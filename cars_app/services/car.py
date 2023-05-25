from http import HTTPStatus

from fastapi import Depends, HTTPException
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from cars_app.database.crud.car import CarCRUD
from cars_app.database.settings import get_session
from cars_app.exceptions.constants import MSG_CAR_NOT_FOUND, MSG_LOCATION_NOT_FOUND
from cars_app.validation.schemas import (
    CarInfo,
    CarUpdate,
)


class CarService:
    def __init__(
        self,
        car_crud: CarCRUD,
    ) -> None:
        """Init `CarService` instance."""
        self.car_crud = car_crud

    async def update(self, car_id: int, data: CarUpdate) -> CarInfo:
        """Update specific car."""
        try:
            updated_car = await self.car_crud.update(car_id, data)
            return updated_car
        except NoResultFound:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=MSG_CAR_NOT_FOUND,
            )
        except IntegrityError as e:
            if 'ForeignKeyViolationError' in str(e.orig):
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND,
                    detail=MSG_LOCATION_NOT_FOUND,
                )
            else:
                raise


def get_car_service(session: AsyncSession = Depends(get_session)):
    """Returns `CarService` instance."""
    car_crud = CarCRUD(session)
    return CarService(car_crud)
