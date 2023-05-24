import aiofiles

import csv
from aiocsv import AsyncDictReader

from sqlalchemy.ext.asyncio import AsyncSession

from cars_app.database.crud.location import LocationCRUD
from cars_app.database.models import Location
from cars_app.validation.schemas import LocationCreate


class HelperService:
    def __init__(self, location_crud: LocationCRUD) -> None:
        self.location_crud = location_crud

    async def populate_locations(self):
        if not await self._is_populated_with_locations():
            locations_list = await self.read_from_source()
            for location in locations_list:
                location_data = LocationCreate(
                    city=location['city'],
                    state=location['state_name'],
                    zip_code=int(location['zip']),
                    latitude=float(location['lat']),
                    longtitude=float(location['lng']),
                )
                await self.location_crud.create(location_data)

    async def _is_populated_with_locations(self) -> Location | None:
        return await self.location_crud.read_first()

    async def read_from_source(self):
        locations_list = []
        async with aiofiles.open('uszips.csv', mode='r', encoding='utf-8', newline='') as file:
            async for row in AsyncDictReader(file, quoting=csv.QUOTE_ALL):
                locations_list.append(row)
        return locations_list


def get_helper_service(session: AsyncSession):
    location_crud = LocationCRUD(session)
    return HelperService(location_crud)
