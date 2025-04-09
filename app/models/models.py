from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.base import Base

# Association table for movie-genre relationship
movie_genre = Table(
    'movie_genre',
    Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id')),
    Column('genre_id', Integer, ForeignKey('genres.id'))
)

# Association table for movie-actor relationship
movie_actor = Table(
    'movie_actor',
    Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id')),
    Column('actor_id', Integer, ForeignKey('actors.id'))
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
    ratings = relationship("Rating", back_populates="user")
    favorite_genres = relationship("Genre", secondary="user_favorite_genres")
    favorite_actors = relationship("Actor", secondary="user_favorite_actors")

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    release_year = Column(Integer)
    director_id = Column(Integer, ForeignKey('directors.id'))
    
    director = relationship("Director", back_populates="movies")
    genres = relationship("Genre", secondary=movie_genre, back_populates="movies")
    actors = relationship("Actor", secondary=movie_actor, back_populates="movies")
    ratings = relationship("Rating", back_populates="movie")

class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    movies = relationship("Movie", secondary=movie_genre, back_populates="genres")

class Actor(Base):
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    
    movies = relationship("Movie", secondary=movie_actor, back_populates="actors")

class Director(Base):
    __tablename__ = "directors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    
    movies = relationship("Movie", back_populates="director")

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    movie_id = Column(Integer, ForeignKey('movies.id'))
    score = Column(Float)
    
    user = relationship("User", back_populates="ratings")
    movie = relationship("Movie", back_populates="ratings") 