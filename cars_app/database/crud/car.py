from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from cars_app.database.models import Car, Cargo
from cars_app.validation.schemas import CarCreate, CarUpdate


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

    async def create(self, data: CarCreate) -> Car:
        """Create car."""
        car = Car(**data.dict())
        self.session.add(car)
        await self.session.commit()
        await self.session.refresh(car)
        return car

    async def update(self, car_id: int, data: CarUpdate) -> Car:
        """Update specific car."""
        values = data.dict(exclude_unset=True)
        stmt = update(Car).where(Car.id == car_id).values(**values).returning(Car)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def get_car_location_coordinates(self, car: Car) -> tuple[float]:
        """Returns car's current locations coordinates."""
        query = select(car.location_relation.latitude, car.location_relation.longtitude)
        result = await self.session.execute(query)
        return result.scalar_one()
