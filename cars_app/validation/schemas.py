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


# Cargo
class CargoBase(BaseModel):
    pickup_location: int
    delivery_location: int


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


class CargoListElement(CargoBase):
    cars_count: int


class CargoInfoDetail(CargoCreate):
    cars: list[CarPlate]


# Errors
class CodelessErrorResponseModel(BaseModel):
    message: str


class ErrorResponseModel(BaseModel):
    code: int
    message: str
