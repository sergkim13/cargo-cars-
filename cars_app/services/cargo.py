from http import HTTPStatus

from fastapi import Depends, HTTPException
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from cars_app.database.crud.cargo import CargoCRUD
from cars_app.database.models import Cargo
from cars_app.database.settings import get_session
from cars_app.exceptions.constants import MSG_CARGO_NOT_FOUND, MSG_LOCATION_NOT_FOUND
from cars_app.validation.schemas import CargoCreate, CargoInfo, CargoInfoDetail, CargoList, CargoUpdate


class CargoService:
    def __init__(
        self,
        cargo_crud: CargoCRUD,
    ) -> None:
        """Init `CargoService` instance."""
        self.cargo_crud = cargo_crud

    async def get_list(self) -> CargoList:
        """Gets list of cargos and returns serialized response."""
        cargos = await self.cargo_crud.read_all()
        return cargos
    
    async def get_detail(self, cargo_id: int) -> CargoInfoDetail:
        """Gets info about specific cargo."""
        try:
            cargo = await self.cargo_crud.read(cargo_id=cargo_id)
            # await self.cache.set(cache_key, user)
        except NoResultFound:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=MSG_CARGO_NOT_FOUND,
            )
        return cargo

    async def create(self, data: CargoCreate) -> CargoInfo:
        """Creates new cargo."""
        try:
            user = await self.cargo_crud.create(data=data)
            # await self.cache.clear('all')
            return user
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


def get_cargo_service(session: AsyncSession = Depends(get_session)):
    cargo_crud = CargoCRUD(session)
    return CargoService(cargo_crud)
