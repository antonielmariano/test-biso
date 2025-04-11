from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.base import get_db
from app.core.auth import get_current_active_user
from app.models.movie import Movie
from app.models.rating import Rating
from app.models.user import User
from app.schemas.ratings import RatingCreate, RatingSchema

router = APIRouter()

@router.post("/", response_model=RatingSchema)
def create_rating(
    rating: RatingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    movie = db.query(Movie).filter(Movie.id == rating.movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
        
    existing_rating = db.query(Rating).filter(
        Rating.user_id == current_user.id,
        Rating.movie_id == rating.movie_id
    ).first()
    
    if existing_rating:
        existing_rating.score = rating.score
        db.commit()
        db.refresh(existing_rating)
        return existing_rating
        
    db_rating = Rating(
        user_id=current_user.id,
        movie_id=rating.movie_id,
        score=rating.score
    )
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating

@router.get("/user", response_model=List[RatingSchema])
def get_user_ratings(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):  
    ratings = db.query(Rating).filter(
        Rating.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    return ratings

@router.get("/movie/{movie_id}", response_model=List[RatingSchema])
def get_movie_ratings(
    movie_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    ratings = db.query(Rating).filter(
        Rating.movie_id == movie_id
    ).offset(skip).limit(limit).all()
    return ratings

@router.get("/movie/{movie_id}/average", response_model=float)
def get_movie_average_rating(
    movie_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    ratings = db.query(Rating).filter(
        Rating.movie_id == movie_id
    ).all()
    
    if not ratings:
        return 0.0
        
    total_score = sum(rating.score for rating in ratings)
    return total_score / len(ratings) 