from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from typing import List

from app.models.movie import Movie

class Director(Base):
    __tablename__ = "directors"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True)
    
    movies: Mapped[List[Movie]] = relationship(back_populates="director")