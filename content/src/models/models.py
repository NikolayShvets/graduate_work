from datetime import date

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    String,
    Table,
    Enum, Text, text, Float, CheckConstraint, Date, func, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base, mapper_registry
from models.constance import VideoType, Role


genre_film_work = Table(
    "genrefilmwork",
    Base.metadata,
    Column("id", UUID, primary_key=True, server_default=text("gen_random_uuid()")),
    Column("genre_id", ForeignKey("genre.id"), primary_key=True),
    Column("film_work_id", ForeignKey("filmwork.id"), primary_key=True),
    Column("created_at", DateTime(timezone=False), server_default=func.now()),
    UniqueConstraint("genre_id", "film_work_id")
)


person_film_work = Table(
    "personfilmwork",
    Base.metadata,
    Column("id", UUID, primary_key=True, server_default=text("gen_random_uuid()")),
    Column("person_id", ForeignKey("person.id"), primary_key=True),
    Column("film_work_id", ForeignKey("filmwork.id"), primary_key=True),
    Column("role", Enum(Role), nullable=False),
    Column("created_at", DateTime(timezone=False), server_default=func.now()),
    UniqueConstraint("person_id", "film_work_id", "role")
)


class GenreFilmWork:
    pass


class PersonFilmWork:
    pass


mapper_registry.map_imperatively(GenreFilmWork, genre_film_work)
mapper_registry.map_imperatively(PersonFilmWork, person_film_work)


class Genre(Base):
    name: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    films = relationship("FilmWork", secondary=genre_film_work, back_populates="genres")


class Person(Base):
    full_name: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)

    films = relationship("FilmWork", secondary=person_film_work, back_populates="persons")


class FilmWork(Base):
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    creation_date: Mapped[date] = mapped_column(Date, nullable=False)
    rating: Mapped[float] = mapped_column(Float, CheckConstraint("rating > 0 AND rating <=10"), nullable=False)
    type: Mapped[str] = mapped_column(Enum(VideoType), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    genres: Mapped[list["Genre"]] = relationship("Genre", secondary=genre_film_work, back_populates="films")
    persons: Mapped[list["Person"]] = relationship("Person", secondary=person_film_work, back_populates="films")


