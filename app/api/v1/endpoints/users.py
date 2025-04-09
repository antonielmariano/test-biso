from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.base import get_db
from app.schemas import schemas
from app.models import models
from app.core.security import get_password_hash
from app.core.auth import get_current_active_user

router = APIRouter()

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
        
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/", response_model=List[schemas.User])
def get_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

@router.get("/{user_id}", response_model=schemas.User)
def get_user(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/{user_id}/favorite-genres/{genre_id}")
def add_favorite_genre(
    user_id: int,
    genre_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Add a genre to user's favorites"""
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this user")
        
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    genre = db.query(models.Genre).filter(models.Genre.id == genre_id).first()
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
        
    if genre not in user.favorite_genres:
        user.favorite_genres.append(genre)
        db.commit()
    return {"message": "Genre added to favorites"}

@router.post("/{user_id}/favorite-actors/{actor_id}")
def add_favorite_actor(
    user_id: int,
    actor_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Add an actor to user's favorites"""
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this user")
        
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    actor = db.query(models.Actor).filter(models.Actor.id == actor_id).first()
    if not actor:
        raise HTTPException(status_code=404, detail="Actor not found")
        
    if actor not in user.favorite_actors:
        user.favorite_actors.append(actor)
        db.commit()
    return {"message": "Actor added to favorites"} 