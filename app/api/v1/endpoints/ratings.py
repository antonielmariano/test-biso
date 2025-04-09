from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.base import get_db
from app.schemas import schemas
from app.models import models
from app.core.auth import get_current_active_user

router = APIRouter()

@router.post("/", response_model=schemas.Rating)
def create_rating(
    rating: schemas.RatingCreate,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to create ratings for this user")
        
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    movie = db.query(models.Movie).filter(models.Movie.id == rating.movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
        
    existing_rating = db.query(models.Rating).filter(
        models.Rating.user_id == user_id,
        models.Rating.movie_id == rating.movie_id
    ).first()
    
    if existing_rating:
        existing_rating.score = rating.score
        db.commit()
        db.refresh(existing_rating)
        return existing_rating
        
    db_rating = models.Rating(
        user_id=user_id,
        movie_id=rating.movie_id,
        score=rating.score
    )
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating

@router.get("/user/{user_id}", response_model=List[schemas.Rating])
def get_user_ratings(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access ratings for this user")
        
    ratings = db.query(models.Rating).filter(
        models.Rating.user_id == user_id
    ).offset(skip).limit(limit).all()
    return ratings

@router.get("/movie/{movie_id}", response_model=List[schemas.Rating])
def get_movie_ratings(
    movie_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    ratings = db.query(models.Rating).filter(
        models.Rating.movie_id == movie_id
    ).offset(skip).limit(limit).all()
    return ratings

@router.get("/movie/{movie_id}/average", response_model=float)
def get_movie_average_rating(
    movie_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    ratings = db.query(models.Rating).filter(
        models.Rating.movie_id == movie_id
    ).all()
    
    if not ratings:
        return 0.0
        
    total_score = sum(rating.score for rating in ratings)
    return total_score / len(ratings) 