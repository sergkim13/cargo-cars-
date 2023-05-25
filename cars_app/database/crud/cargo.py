from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from cars_app.database.models import Cargo
from cars_app.validation.schemas import CargoCreate, CargoUpdate


class CargoCRUD:
    """`Cargo` class which provides CRUD operations."""

    def __init__(self, session: AsyncSession) -> None:
        """Init `CargoCRUD` instance with given session."""
        self.session = session

    async def read_all(self) -> list[Cargo]:
        """Read all cargos."""
        query = select(Cargo)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_pickup_location_coordinates(self, cargo: Cargo) -> tuple:
        """Returns cargo's pickup location coordinates."""
        query = select(cargo.pickup_location_relation)
        result = self.session.execute(query)
        pickup_location = result.scalar_one()
        return (pickup_location.latitude, pickup_location.longtitude)

    async def read(self, cargo_id=int) -> Cargo:
        """Read specific cargo by `id` field."""
        query = select(Cargo).where(Cargo.id == cargo_id)
        result = await self.session.execute(query)
        return result.scalar_one()

    async def create(self, data: CargoCreate) -> Cargo:
        """Create new cargo."""
        cargo = Cargo(**data.dict())
        self.session.add(cargo)
        await self.session.commit()
        await self.session.refresh(cargo)
        return cargo

    async def update(self, cargo_id: int, data: CargoUpdate) -> Cargo:
        """Update specific cargo."""
        values = data.dict(exclude_unset=True)
        stmt = update(Cargo).where(Cargo.id == cargo_id).values(**values).returning(
            Cargo.id,
            Cargo.pickup_location,
            Cargo.delivery_location,
            Cargo.weight,
            Cargo.description,
        )
        result = await self.session.execute(stmt)
        return result.fetchone()

    async def delete(self, cargo_id: int):
        """Delete specific cargo."""
        cargo = await self.read(cargo_id)
        await self.session.delete(cargo)
        await self.session.commit()
