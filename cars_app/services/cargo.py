from http import HTTPStatus

from fastapi import Depends, HTTPException
from geopy.distance import distance
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from cars_app.database.crud.car import CarCRUD
from cars_app.database.crud.cargo import CargoCRUD
from cars_app.database.crud.location import LocationCRUD
from cars_app.database.models import Car, Cargo, Location
from cars_app.database.settings import get_session
from cars_app.exceptions.constants import MSG_CARGO_NOT_FOUND, MSG_LOCATION_NOT_FOUND
from cars_app.services.constants import MAX_DISTANCE_IN_MILES
from cars_app.validation.schemas import (
    CargoCarsInfo,
    CargoCreate,
    CargoInfo,
    CargoInfoDetail,
    CargoListElement,
    CargoUpdate,
)


class CargoService:
    def __init__(
        self,
        cargo_crud: CargoCRUD,
        car_crud: CarCRUD,
        location_crud: LocationCRUD,
    ) -> None:
        """Init `CargoService` instance."""
        self.cargo_crud = cargo_crud
        self.car_crud = car_crud
        self.location_crud = location_crud

    async def get_list(self) -> list[CargoListElement]:
        """Gets list of cargos and returns serialized response."""
        cargos = await self.cargo_crud.read_all()
        serialized_cargos = [
            CargoListElement(
                pickup_location=cargo.pickup_location,
                delivery_location=cargo.delivery_location,
                nearby_cars_count=await self._count_nearby_cars(cargo),
            ) for cargo in cargos
        ]

        return serialized_cargos

    async def get_detail(self, cargo_id: int) -> CargoInfoDetail:
        """Gets info about specific cargo."""
        try:
            cargo = await self.cargo_crud.read(cargo_id=cargo_id)
            cars = await self.car_crud.read_all()
            cars_info = [
                CargoCarsInfo(
                    number_plate=car.number_plate,
                    distance_to_cargo=await self._count_distance(car, cargo),
                ) for car in cars
            ]
            # await self.cache.set(cache_key, user)
        except NoResultFound:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=MSG_CARGO_NOT_FOUND,
            )
        return CargoInfoDetail(
            id=cargo.id,
            pickup_location=cargo.pickup_location,
            delivery_location=cargo.delivery_location,
            weight=cargo.weight,
            description=cargo.description,
            cars_info=cars_info,
        )

    async def create(self, data: CargoCreate) -> CargoInfo:
        """Creates new cargo."""
        try:
            cargo = await self.cargo_crud.create(data=data)
            # await self.cache.clear('all')
            return cargo
        except IntegrityError as e:
            if 'ForeignKeyViolationError' in str(e.orig):
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND,
                    detail=MSG_LOCATION_NOT_FOUND,
                )
            else:
                raise

    async def update(self, cargo_id: int, data: CargoUpdate) -> CargoInfo:
        """Update specific cargo."""
        try:
            updated_user = await self.cargo_crud.update(cargo_id, data)
            return updated_user
        except NoResultFound:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=MSG_CARGO_NOT_FOUND,
            )

    async def delete(self, cargo_id: int) -> None:
        """Delete cargo."""
        try:
            await self.cargo_crud.delete(cargo_id)
            # await self.cache.clear(f'user-{user_id}')
            # await self.cache.clear('all')
        except NoResultFound:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=MSG_CARGO_NOT_FOUND,
            )

    async def _count_nearby_cars(self, cargo: Cargo, max_distance_in_miles: int = MAX_DISTANCE_IN_MILES) -> int:
        """Returns count of cars in `max_distance_in_miles` from cargo."""
        cars = await self.car_crud.read_all()
        nearby_cars = [car for car in cars if await self._count_distance(car, cargo) <= max_distance_in_miles]
        return len(nearby_cars)

    async def _count_distance(self, car: Car, cargo: Cargo) -> float:
        """Count distance in miles between given car and cargo."""
        car_location = await self._get_location(car.current_location)
        cargo_location = await self._get_location(cargo.pickup_location)
        car_coordinates = (car_location.latitude, car_location.longtitude)
        cargo_coordinates = (cargo_location.latitude, cargo_location.longtitude)
        return distance(car_coordinates, cargo_coordinates).miles

    async def _get_location(self, location_zip: int) -> Location:
        """Returns location with given zip_code."""
        try:
            location = await self.location_crud.read(location_zip)
            return location
        except NoResultFound:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=MSG_LOCATION_NOT_FOUND,
            )


def get_cargo_service(session: AsyncSession = Depends(get_session)):
    """Returns `CargoService` instance."""
    cargo_crud = CargoCRUD(session)
    car_crud = CarCRUD(session)
    location_crud = LocationCRUD(session)
    return CargoService(cargo_crud, car_crud, location_crud)
