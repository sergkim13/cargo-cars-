import csv
import random
import string

import aiofiles  # type: ignore
from aiocsv import AsyncDictReader
from sqlalchemy.ext.asyncio import AsyncSession

from cars_app.database.crud.car import CarCRUD
from cars_app.database.crud.location import LocationCRUD
from cars_app.database.models import Car, Location
from cars_app.logging.module import logger
from cars_app.validation.schemas import CarCreate, LocationCreate


class HelperService:
    def __init__(self, location_crud: LocationCRUD, car_crud: CarCRUD) -> None:
        self.location_crud = location_crud
        self.car_crud = car_crud

    async def populate_locations(self):
        if not await self._is_populated_with_locations():
            locations_list = await self._read_locations_from_source()
            for location in locations_list:
                location_data = LocationCreate(
                    city=location['city'],
                    state=location['state_name'],
                    zip_code=int(location['zip']),
                    latitude=float(location['lat']),
                    longtitude=float(location['lng']),
                )
                await self.location_crud.create(location_data)
        logger.info('Локации загружены в БД.')

    async def populate_cars(self):
        if not await self._is_populated_with_cars():
            cars_list = await self._generate_cars()
            for car in cars_list:
                await self.car_crud.create(car)
        logger.info('Машины загружены в БД.')

    async def _read_locations_from_source(self):
        locations_list = []
        async with aiofiles.open('uszips.csv', mode='r', encoding='utf-8', newline='') as file:
            async for row in AsyncDictReader(file, quoting=csv.QUOTE_ALL):
                locations_list.append(row)
        return locations_list

    async def _generate_cars(self):
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
        number_plates: set[str] = set()
        while len(number_plates) < 20:
            number = random.randint(1000, 9999)
            letter = random.choice(string.ascii_uppercase)
            number_plates.add(f'{number}{letter}')
        return list(number_plates)

    async def _get_location_zips(self) -> list:
        zips: list[int] = []
        locations_list = await self._read_locations_from_source()
        while len(zips) < 20:
            random_location = random.choice(locations_list)
            zips.append(random_location['zip'])
        return zips

    async def _is_populated_with_locations(self) -> Location | None:
        return await self.location_crud.read_first()

    async def _is_populated_with_cars(self) -> Car | None:
        return await self.car_crud.read_first()


def get_helper_service(session: AsyncSession):
    location_crud = LocationCRUD(session)
    car_crud = CarCRUD(session)
    return HelperService(location_crud, car_crud)
