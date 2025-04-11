from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from typing import List

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.actor import Actor
    from app.models.genre import Genre
    from app.models.rating import Rating
    from app.models.director import Director



movie_genre = Table(
    'movie_genre',
    Base.metadata,
    Column('movie_id', ForeignKey('movies.id')),
    Column('genre_id', ForeignKey('genres.id'))
)

movie_actor = Table(
    'movie_actor',
    Base.metadata,
    Column('movie_id', ForeignKey('movies.id')),
    Column('actor_id', ForeignKey('actors.id'))
)

class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(index=True)
    description: Mapped[str]
    release_year: Mapped[int]
    director_id: Mapped[int] = mapped_column(ForeignKey('directors.id'))
    
    director: Mapped["Director"] = relationship(back_populates="movies")
    genres: Mapped[List["Genre"]] = relationship(secondary=movie_genre, back_populates="movies")
    actors: Mapped[List["Actor"]] = relationship(secondary=movie_actor, back_populates="movies")
    ratings: Mapped[List["Rating"]] = relationship(back_populates="movie")








