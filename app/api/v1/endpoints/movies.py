from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.base import get_db
from app.schemas import schemas
from app.models import models
from app.core.auth import get_current_active_user
from app.services.recommender import MovieRecommender

router = APIRouter()

@router.post("/", response_model=schemas.Movie)
def create_movie(
    movie: schemas.MovieCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_movie = models.Movie(
        title=movie.title,
        description=movie.description,
        rating=movie.rating,
        year=movie.year,
        director=movie.director
    )
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

@router.get("/", response_model=List[schemas.Movie])
def get_movies(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    movies = db.query(models.Movie).offset(skip).limit(limit).all()
    return movies

@router.get("/{movie_id}", response_model=schemas.Movie)
def get_movie(
    movie_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.post("/{movie_id}/rate", response_model=schemas.Rating)
def rate_movie(
    movie_id: int,
    rating: schemas.RatingCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    existing_rating = db.query(models.Rating).filter(
        models.Rating.user_id == current_user.id,
        models.Rating.movie_id == movie_id
    ).first()
    
    if existing_rating:
        existing_rating.rating = rating.rating
        db.commit()
        db.refresh(existing_rating)
        return existing_rating
    
    db_rating = models.Rating(
        rating=rating.rating,
        user_id=current_user.id,
        movie_id=movie_id
    )
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating

@router.get("/recommendations/", response_model=List[schemas.Movie])
def get_recommendations(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    recommender = MovieRecommender(db)
    recommended_movies = recommender.get_recommendations(current_user.id)
    return recommended_movies 