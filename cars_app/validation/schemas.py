import re

from pydantic import BaseModel, Field, validator


# Location
class LocationDetail(BaseModel):
    city: str
    state: str
    zip_code: int
    latitude: float
    longtitude: float


class LocationCreate(LocationDetail):
    pass


# Car
class CarPlate(BaseModel):
    number_plate: str

    @validator('number_plate')
    def validate_number_plate(cls, v):
        if not re.match('^[1-9][0-9]{3}[A-Z]$', v):
            raise ValueError('Invalid number plate')
        return v


class CarUpdate(BaseModel):
    current_location: int


class CarCreate(CarPlate):
    current_location: int
    capacity: int = Field(ge=1, le=1000)


class CarInfo(BaseModel):
    id: int
    number_plate: str
    current_location: int
    capacity: int = Field(ge=1, le=1000)

    @validator('number_plate')
    def validate_number_plate(cls, v):
        if not re.match('^[1-9][0-9]{3}[A-Z]$', v):
            raise ValueError('Invalid number plate')
        return v

    class Config:
        orm_mode = True


# Cargo
class CargoBase(BaseModel):
    pickup_location: int
    delivery_location: int

    class Config:
        orm_mode = True


class CargoCreate(CargoBase):
    weight: int = Field(ge=1, le=1000)
    description: str


class CargoInfo(BaseModel):
    id: int
    pickup_location: int
    delivery_location: int
    weight: int = Field(ge=1, le=1000)
    description: str

    class Config:
        orm_mode = True


class CargoUpdate(BaseModel):
    weight: int = Field(ge=1, le=1000)
    description: str


class CargoListElement(BaseModel):
    id: int
    pickup_location: int
    delivery_location: int
    nearby_cars_count: int

    class Config:
        orm_mode = True


class CargoCarsInfo(CarPlate):
    distance_to_cargo: float

    @validator('distance_to_cargo')
    def round_distance(cls, v):
        return round(v, 2)


class CargoInfoDetail(CargoInfo):
    cars_info: list[CargoCarsInfo]
