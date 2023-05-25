from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cars_app.database.models import Car, Cargo
from cars_app.validation.schemas import CarCreate


class CarCRUD:
    """`CarCRUD` class which provides CRUD operations."""

    def __init__(self, session: AsyncSession) -> None:
        """Init `CarCRUD` instance with given session."""
        self.session = session

    async def read_all(self) -> list[Cargo]:
        query = select(Car)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def read_first(self) -> Car | None:
        query = select(Car)
        result = await self.session.execute(query)
        return result.first()

    async def create(self, data: CarCreate) -> None:
        """Create car."""
        car = Car(**data.dict())
        self.session.add(car)
        await self.session.commit()

    async def get_car_location_coordinates(self, car: Car) -> tuple[float]:
        """Returns car's current locations coordinates."""
        query = select(car.location_relation.latitude, car.location_relation.longtitude)
        result = await self.session.execute(query)
        return result.scalar_one()
