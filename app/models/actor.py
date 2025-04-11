from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from typing import List

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.movie import Movie

from app.models.movie import movie_actor


class Actor(Base):
    __tablename__ = "actors"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True)
    
    movies: Mapped[List["Movie"]] = relationship(secondary=movie_actor, back_populates="actors")

