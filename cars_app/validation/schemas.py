import re

from fastapi import HTTPException, Query
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


class CarUpdateBulk(BaseModel):
    id: int
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


# Query
class QueryParams(BaseModel):
    weight_min: int = Query(default=1, ge=1, le=1000)
    weight_max: int = Query(default=1000, ge=1, le=1000)
    distance_min: int = Query(default=0, ge=0)
    distance_max: int = Query(default=450, ge=0)

    @validator('weight_max')
    def validate_weight_max(cls, v, values):
        if v < values['weight_min']:
            raise HTTPException(
                status_code=422,
                detail='weight_max должен быть больше или равен weight_min',
            )
        return v

    @validator('distance_max')
    def validate_distance_max(cls, v, values):
        if v < values['distance_min']:
            raise HTTPException(
                status_code=422,
                detail='distance_max должен быть больше или равен distance_min',
            )
        return v
