from http import HTTPStatus

from fastapi import Depends, HTTPException
from geopy.distance import distance
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from cars_app.cache.abstract_cache import AbstractCache
from cars_app.cache.module import get_redis_cache
from cars_app.database.crud.car import CarCRUD
from cars_app.database.crud.cargo import CargoCRUD
from cars_app.database.crud.location import LocationCRUD
from cars_app.database.models import Car, Cargo, Location
from cars_app.database.settings import get_session
from cars_app.exceptions.constants import MSG_CARGO_NOT_FOUND, MSG_LOCATION_NOT_FOUND
from cars_app.validation.schemas import (
    CargoCarsInfo,
    CargoCreate,
    CargoInfo,
    CargoInfoDetail,
    CargoListElement,
    CargoUpdate,
    QueryParams,
)


class CargoService:
    def __init__(
        self,
        cargo_crud: CargoCRUD,
        car_crud: CarCRUD,
        location_crud: LocationCRUD,
        cache: AbstractCache,
    ) -> None:
        """Init `CargoService` instance."""
        self.cargo_crud = cargo_crud
        self.car_crud = car_crud
        self.location_crud = location_crud
        self.cache = cache

    async def get_list(self, query: QueryParams) -> list[CargoListElement]:
        """Gets list of cargos and returns serialized response."""
        cache_key = f'cargo-{query}'
        serialized_cargos = await self.cache.get(cache_key)
        if not serialized_cargos:
            cargos = await self.cargo_crud.read_all(query.weight_min, query.weight_max)
            serialized_cargos = [
                CargoListElement(
                    id=cargo.id,
                    pickup_location=cargo.pickup_location,
                    delivery_location=cargo.delivery_location,
                    nearby_cars_count=await self._count_nearby_cars(cargo, query.distance_min, query.distance_max),
                ) for cargo in cargos
            ]
            await self.cache.set(cache_key, serialized_cargos)

        return serialized_cargos

    async def get_detail(self, cargo_id: int) -> CargoInfoDetail:
        """Gets info about specific cargo."""
        cache_key = f'cargo-{cargo_id}'
        cargo_detail = await self.cache.get(cache_key)
        if not cargo_detail:
            try:
                cargo = await self.cargo_crud.read(cargo_id=cargo_id)
                cars = await self.car_crud.read_all()
                cars_info = [
                    CargoCarsInfo(
                        number_plate=car.number_plate,
                        distance_to_cargo=await self._count_distance(car, cargo),
                    ) for car in cars
                ]
                cargo_detail = CargoInfoDetail(
                    id=cargo.id,
                    pickup_location=cargo.pickup_location,
                    delivery_location=cargo.delivery_location,
                    weight=cargo.weight,
                    description=cargo.description,
                    cars_info=cars_info,
                )
                await self.cache.set(cache_key, cargo_detail)
            except NoResultFound:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND,
                    detail=MSG_CARGO_NOT_FOUND,
                )
        return cargo_detail

    async def create(self, data: CargoCreate) -> CargoInfo:
        """Creates new cargo."""
        try:
            cargo = await self.cargo_crud.create(data=data)
            await self.cache.clear('all')
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
            updated_cargo = await self.cargo_crud.update(cargo_id, data)
            await self.cache.clear(f'cargo-{cargo_id}')
            await self.cache.clear('all')
            return updated_cargo
        except NoResultFound:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=MSG_CARGO_NOT_FOUND,
            )

    async def delete(self, cargo_id: int) -> None:
        """Delete cargo."""
        try:
            await self.cargo_crud.delete(cargo_id)
            await self.cache.clear(f'cargo-{cargo_id}')
            await self.cache.clear('all')
        except NoResultFound:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=MSG_CARGO_NOT_FOUND,
            )

    async def _count_nearby_cars(self, cargo: Cargo, distance_min: int, distance_max: int) -> int:
        """Returns count of cars which are between `distance_min` and `distance_max` from cargo."""
        cars = await self.car_crud.read_all()
        nearby_cars = [
            car for car in cars
            if await self._count_distance(car, cargo) >= distance_min
            and await self._count_distance(car, cargo) <= distance_max
        ]
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


def get_cargo_service(
        session: AsyncSession = Depends(get_session),
        cache: AbstractCache = Depends(get_redis_cache),
):
    """Returns `CargoService` instance."""
    cargo_crud = CargoCRUD(session)
    car_crud = CarCRUD(session)
    location_crud = LocationCRUD(session)
    return CargoService(cargo_crud, car_crud, location_crud, cache)
