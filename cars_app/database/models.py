from geopy.distance import distance
from sqlalchemy import CheckConstraint, Float, ForeignKey, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Location(Base):
    __tablename__ = 'location'

    zip_code: Mapped[int] = mapped_column(Integer, primary_key=True)
    city: Mapped[str] = mapped_column(String(32))
    state: Mapped[str] = mapped_column(String(32))
    latitude: Mapped[float] = mapped_column(Float)
    longtitude: Mapped[float] = mapped_column(Float)

    car_relation: Mapped[list['Car']] = relationship(
        back_populates='location_relation',
        cascade='all, delete-orphan',
        lazy='joined',
    )

    def __repr__(self) -> str:
        return f'Location(id={self.id!r}, zip_code={self.zip_code!r})'


class Cargo(Base):
    __tablename__ = 'cargo'
    __table_args__ = (
        CheckConstraint('weight >= 1', name='check_weight_min'),
        CheckConstraint('weight <= 1000', name='check_weight_max'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pickup_location: Mapped[int] = mapped_column(ForeignKey('location.zip_code'))
    delivery_location: Mapped[int] = mapped_column(ForeignKey('location.zip_code'))
    weight: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(String(512))

    pickup_location_relation: Mapped['Location'] = relationship(
        foreign_keys=[pickup_location],
    )
    delivery_location_relation: Mapped['Location'] = relationship(
        foreign_keys=[delivery_location],
    )

    def __repr__(self) -> str:
        return f'Cargo(id={self.id!r})'


class Car(Base):
    __tablename__ = 'car'
    __table_args__ = (
        CheckConstraint('capacity >= 1', name='check_capacity_min'),
        CheckConstraint('capacity <= 1000', name='check_capacity_max'),
        CheckConstraint("number_plate ~ '^[1-9][0-9]{3}[A-Z]$'", name='check_number_plate_pattern'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    number_plate: Mapped[str] = mapped_column(String(32), unique=True)
    current_location: Mapped[int] = mapped_column(ForeignKey('location.zip_code'))
    capacity: Mapped[int] = mapped_column(Integer)

    location_relation: Mapped['Location'] = relationship(
        back_populates='car_relation',
    )

    @hybrid_property
    def distance_to_cargo(self, cargo: Cargo):
        car_coordinates = (self.location_relation.latitude, self.location_relation.longtitude)
        cargo_coordinates = (cargo.pickup_location_relation.latitude,
                             cargo.pickup_location_relation.longtitude)
        return distance(car_coordinates, cargo_coordinates).miles

    def __repr__(self) -> str:
        return f'Car(id={self.id!r})'
