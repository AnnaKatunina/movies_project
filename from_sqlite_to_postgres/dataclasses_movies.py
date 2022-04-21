import datetime
import uuid
from dataclasses import dataclass, fields


@dataclass(frozen=True)
class CommonDataclass:

    @classmethod
    def fields_names(cls):
        fields_names = [field.name for field in fields(cls)]
        return ', '.join(fields_names)

    @classmethod
    def amount_of_fields(cls):
        amount_of_fields = fields(cls)
        return len(amount_of_fields)


@dataclass(frozen=True)
class Person(CommonDataclass):
    id: uuid.UUID
    full_name: str
    birth_date: datetime.date
    created: datetime.datetime
    modified: datetime.datetime


@dataclass(frozen=True)
class Genre(CommonDataclass):
    id: uuid.UUID
    name: str
    description: str
    created: datetime.datetime
    modified: datetime.datetime


@dataclass(frozen=True)
class Filmwork(CommonDataclass):
    id: uuid.UUID
    title: str
    description: str
    creation_date: datetime.date
    certificate: str
    file_path: str
    rating: float
    type: str
    created: datetime.datetime
    modified: datetime.datetime


@dataclass(frozen=True)
class GenreFilmwork(CommonDataclass):
    id: uuid.UUID
    film_work_id: uuid.UUID
    genre_id: uuid.UUID
    created: datetime.datetime


@dataclass(frozen=True)
class PersonFilmwork(CommonDataclass):
    id: uuid.UUID
    film_work_id: uuid.UUID
    person_id: uuid.UUID
    role: str
    created: datetime.datetime
