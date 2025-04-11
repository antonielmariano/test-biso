from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from datetime import datetime
from typing import List

from app.models.actor import Actor
from app.models.genre import Genre
from app.models.rating import Rating

user_favorite_genres = Table(
    "user_favorite_genres",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("genre_id", ForeignKey("genres.id"), primary_key=True)
)

user_favorite_actors = Table(
    "user_favorite_actors",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("actor_id", ForeignKey("actors.id"), primary_key=True)
)

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active: Mapped[bool] = mapped_column(default=True)
    
    ratings: Mapped[List[Rating]] = relationship(back_populates="user")
    favorite_genres: Mapped[List[Genre]] = relationship(secondary="user_favorite_genres")
    favorite_actors: Mapped[List[Actor]] = relationship(secondary="user_favorite_actors")
