import csv
import random
import string

import aiofiles  # type: ignore
from aiocsv import AsyncDictReader
from sqlalchemy.ext.asyncio import AsyncSession

from cars_app.cache.abstract_cache import AbstractCache
from cars_app.cache.module import get_redis_cache
from cars_app.database.crud.car import CarCRUD
from cars_app.database.crud.location import LocationCRUD
from cars_app.database.models import Car, Location
from cars_app.logging.module import logger
from cars_app.validation.schemas import CarCreate, CarUpdateBulk, LocationCreate


class HelperService:
    def __init__(
            self,
            location_crud: LocationCRUD,
            car_crud: CarCRUD,
            cache: AbstractCache
    ) -> None:
        """Inits `HelperService` instance."""
        self.location_crud = location_crud
        self.car_crud = car_crud
        self.cache = cache

    async def populate_locations(self) -> None:
        """Populates database with locations."""
        if not await self._is_populated_with_locations():
            locations_data = await self._read_locations_from_source()
            locations_list = [
                LocationCreate(
                    city=location['city'],
                    state=location['state_name'],
                    zip_code=int(location['zip']),
                    latitude=float(location['lat']),
                    longtitude=float(location['lng']),
                ) for location in locations_data
            ]
            await self.location_crud.create_list(locations_list)
        logger.info('Локации загружены в БД.')

    async def populate_cars(self) -> None:
        """Populates database with cars."""
        if not await self._is_populated_with_cars():
            cars_list = await self._generate_cars()
            await self.car_crud.create_list(cars_list)
        logger.info('Машины загружены в БД.')

    async def update_locations_random(self) -> None:
        """Update current locations of all cars randomly."""
        cars_update_list = []
        cars = await self.car_crud.read_all()
        locations = await self.location_crud.read_all()
        locations_zips = [location.zip_code for location in locations]
        for car in cars:
            avaliable_zips = [
                zip_code for zip_code in locations_zips if zip_code != car.current_location
            ]
            cars_update_list.append(CarUpdateBulk(
                id=car.id, current_location=random.choice(avaliable_zips))
            )
        await self.car_crud.update_list(cars_update_list)
        await self.cache.clear('all')
        logger.info('Локации машин обновлены.')

    async def _read_locations_from_source(self) -> list:
        """Read locations data from 'uszips.csv' file."""
        locations_data = []
        async with aiofiles.open('uszips.csv', mode='r', encoding='utf-8', newline='') as file:
            async for row in AsyncDictReader(file, quoting=csv.QUOTE_ALL):
                locations_data.append(row)
        return locations_data

    async def _generate_cars(self) -> list[CarCreate]:
        """Generate cars data."""
        cars = []
        number_plates = self._get_number_plates()
        zips = await self._get_location_zips()
        for i in range(20):
            car = CarCreate(
                number_plate=number_plates[i],
                current_location=zips[i],
                capacity=random.randint(1, 1000),
            )
            cars.append(car)
        return cars

    def _get_number_plates(self) -> list:
        """Genrate car number plates."""
        number_plates: set[str] = set()
        while len(number_plates) < 20:
            number = random.randint(1000, 9999)
            letter = random.choice(string.ascii_uppercase)
            number_plates.add(f'{number}{letter}')
        return list(number_plates)

    async def _get_location_zips(self) -> list:
        """Get list of locations zip codes."""
        zips: list[int] = []
        locations_list = await self._read_locations_from_source()
        while len(zips) < 20:
            random_location = random.choice(locations_list)
            zips.append(random_location['zip'])
        return zips

    async def _is_populated_with_locations(self) -> Location | None:
        """Checks if database is populated with locations."""
        return await self.location_crud.read_first()

    async def _is_populated_with_cars(self) -> Car | None:
        """Checks if database is populated with cars."""
        return await self.car_crud.read_first()


def get_helper_service(session: AsyncSession):
    """Returns `HelperService` instance."""
    location_crud = LocationCRUD(session)
    car_crud = CarCRUD(session)
    cache = get_redis_cache()
    return HelperService(location_crud, car_crud, cache)
