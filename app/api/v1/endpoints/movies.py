from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.base import get_db
from app.models.actor import Actor
from app.models.director import Director
from app.models.genre import Genre
from app.models.movie import Movie 
from app.models.rating import Rating
from app.core.auth import get_current_active_user
from app.models.user import User
from app.schemas.movies import MovieCreate, MovieSchema
from app.services.recommender import MovieRecommender
from app.schemas.ratings import RatingCreate, RatingSchema

router = APIRouter()

@router.post("/", response_model= MovieSchema)
def create_movie(
    movie: MovieCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_movie = Movie(
        title=movie.title,
        description=movie.description,
        release_year=movie.release_year
    )
    director = db.query(Director).filter_by(name=movie.director_name).first()
    if not director:
        director = Director(name=movie.director_name)
        db.add(director)
        db.commit()
        db.refresh(director)
    
    db_movie.director = director
    db_movie.director_id = director.id

    for actor_name in movie.actors:
        actor = db.query(Actor).filter_by(name=actor_name).first()
        if not actor:
            actor = Actor(name=actor_name)
            db.add(actor)
        db_movie.actors.append(actor)

    for genre_name in movie.genres:
        genre = db.query(Genre).filter_by(name=genre_name).first()
        if not genre:
            genre = Genre(name=genre_name)
            db.add(genre)
        db_movie.genres.append(genre)
    
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie
 
@router.get("/", response_model=List[MovieSchema])
def get_movies(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    movies = db.query(Movie).offset(skip).limit(limit).all()
    return movies
    
@router.get("/recommendations", response_model=List[MovieSchema])
def get_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    recommender = MovieRecommender(db)
    recommended_movies = recommender.get_recommendations(current_user.id)
    return recommended_movies 
        
@router.get("/{movie_id}", response_model=MovieSchema)
def get_movie(
    movie_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.post("/{movie_id}/rate", response_model=RatingSchema)
def rate_movie(
    movie_id: int,
    rating: RatingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    existing_rating = db.query(Rating).filter(
        Rating.user_id == current_user.id,
        Rating.movie_id == movie_id
    ).first()
    
    if existing_rating:
        existing_rating.rating = rating.score
        db.commit()
        db.refresh(existing_rating)
        return existing_rating
    
    db_rating = Rating(
        rating=rating.score,
        user_id=current_user.id,
        movie_id=movie_id
    )
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating

