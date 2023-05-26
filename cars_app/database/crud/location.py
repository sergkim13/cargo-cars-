from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cars_app.database.models import Location
from cars_app.validation.schemas import LocationCreate


class LocationCRUD:
    """`LocationCRUD` class which provides CRUD operations."""

    def __init__(self, session: AsyncSession) -> None:
        """Init `LocationCRUD` instance with given session."""
        self.session = session

    async def read_all(self) -> list[Location]:
        """Read all locations."""
        query = select(Location)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def read(self, location_zip: int) -> Location:
        """Read specific location."""
        query = select(Location).where(Location.zip_code == location_zip)
        result = await self.session.execute(query)
        return result.scalar()

    async def read_first(self) -> Location | None:
        """Read first location."""
        query = select(Location)
        result = await self.session.execute(query)
        return result.first()

    async def create(self, data: LocationCreate) -> None:
        """Create location."""
        location = Location(**data.dict())
        self.session.add(location)
        await self.session.commit()
