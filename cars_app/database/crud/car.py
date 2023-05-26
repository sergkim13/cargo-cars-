from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from cars_app.database.models import Car
from cars_app.validation.schemas import CarCreate, CarUpdate, CarUpdateBulk


class CarCRUD:
    """`CarCRUD` class which provides CRUD operations."""

    def __init__(self, session: AsyncSession) -> None:
        """Init `CarCRUD` instance with given session."""
        self.session = session

    async def read_all(self) -> list[Car]:
        """Read all cars."""
        query = select(Car)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def read_first(self) -> Car | None:
        """Read first car."""
        query = select(Car)
        result = await self.session.execute(query)
        return result.first()

    async def create(self, data: CarCreate) -> Car:
        """Create car."""
        stmt = insert(Car).values(**data.dict()).returning(
            Car.id,
            Car.number_plate,
            Car.current_location,
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.fetchone()

    async def create_list(self, data: list[CarCreate]) -> None:
        """Create list of cars."""
        await self.session.execute(
            insert(Car), [car.dict() for car in data]
        )
        await self.session.commit()

    async def update(self, car_id: int, data: CarUpdate) -> Car:
        """Update specific car."""
        values = data.dict(exclude_unset=True)
        stmt = update(Car).where(Car.id == car_id).values(**values).returning(
            Car.id,
            Car.number_plate,
            Car.current_location,
            Car.capacity,
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.fetchone()

    async def update_list(self, data: list[CarUpdateBulk]) -> None:
        """Updates list of cars."""
        await self.session.execute(
            update(Car), [car.dict() for car in data]
        )
        await self.session.commit()

    async def get_car_location_coordinates(self, car: Car) -> tuple[float]:
        """Returns car's current locations coordinates."""
        query = select(car.location_relation.latitude, car.location_relation.longtitude)
        result = await self.session.execute(query)
        return result.scalar_one()
