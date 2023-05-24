import re
from pydantic import BaseModel, validator


# Car
class CarPlate(BaseModel):
    number_plate: str

    @validator('number_plate')
    def validate_number_plate(cls, v):
        if not re.match('^[1-9][0-9]{3}[A-Z]$', v):
            raise ValueError('Invalid number plate')
        return v


class CarUpdate(BaseModel):
    current_location: str


# Cargo
class CargoBase(BaseModel):
    pickup_location: str
    delivery_location: str


class CargoCreate(CargoBase):
    weight: int
    description: str


class CargoUpdate(BaseModel):
    weight: int | None
    description: str | None


class CargoListElement(CargoBase):
    cars_count: int


class CargoList(BaseModel):
    cargos: list[CargoListElement]


class CargoDetail(CargoCreate):
    cars: list[CarPlate]


# Location
class LocationCreate(BaseModel):
    city: str
    state: str
    zip_code: int
    latitude: float
    longtitude: float
