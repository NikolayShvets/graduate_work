from datetime import date

from sqlalchemy import (
    CheckConstraint,
    Column,
    Date,
    Enum,
    Float,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from models.constance import Role, VideoType


class GenreFilmWork(Base):
    genre_id = Column("genre_id", ForeignKey("genre.id"), primary_key=True)
    film_work_id = Column("film_work_id", ForeignKey("filmwork.id"), primary_key=True)

    genre = relationship("Genre", back_populates="films")
    film = relationship("FilmWork", back_populates="genres")


class PersonFilmWork(Base):
    person_id = Column("person_id", ForeignKey("person.id"), primary_key=True)
    film_work_id = Column("film_work_id", ForeignKey("filmwork.id"), primary_key=True)
    role = Column("role", Enum(Role), nullable=False)

    person = relationship("Person", back_populates="films")
    film = relationship("FilmWork", back_populates="persons")


class Genre(Base):
    name: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    films = relationship("GenreFilmWork", back_populates="genre")

    def __str__(self):
        return f"Genre ({self.id}) {self.name}"


class Person(Base):
    full_name: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)

    films = relationship("PersonFilmWork", back_populates="person")

    def __str__(self):
        return f"Person ({self.id}) {self.full_name}"


class FilmWork(Base):
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    creation_date: Mapped[date] = mapped_column(Date, nullable=False)
    rating: Mapped[float] = mapped_column(
        Float, CheckConstraint("rating > 0 AND rating <=10"), nullable=False
    )
    type: Mapped[str] = mapped_column(Enum(VideoType), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    genres = relationship("GenreFilmWork", back_populates="film")
    persons = relationship("PersonFilmWork", back_populates="film")

    def __str__(self) -> str:
        return f"FilmWork ({self.id}) '{self.title}' {self.type} {self.rating}"
