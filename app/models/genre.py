from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from typing import List

from app.models.movie import Movie,movie_genre

class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    
    movies: Mapped[List[Movie]] = relationship(secondary=movie_genre, back_populates="genres")