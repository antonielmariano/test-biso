from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.db.base import get_db
from app.core.security import get_password_hash
from app.core.auth import get_current_active_user
from app.models.actor import Actor
from app.models.genre import Genre
from app.models.user import User
from app.schemas.users import UserOut, UserSchema, UserCreate

router = APIRouter()

@router.post("/", response_model= UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
        
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        name=user.name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/", response_model=List[UserSchema])
def get_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.get("/{user_id}", response_model=UserOut)
def get_user(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    user = db.query(User)\
           .options(
               joinedload(User.favorite_genres),
               joinedload(User.favorite_actors)
           )\
           .filter(User.id == user_id)\
           .first()
       
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@router.post("/{user_id}/favorite-genres/{genre_id}")
def add_favorite_genre(
    user_id: int,
    genre_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this user")
        
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    genre = db.query(Genre).filter(Genre.id == genre_id).first()
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
    current_user: User = Depends(get_current_active_user)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this user")
        
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    actor = db.query(Actor).filter(Actor.id == actor_id).first()
    if not actor:
        raise HTTPException(status_code=404, detail="Actor not found")
        
    if actor not in user.favorite_actors:
        user.favorite_actors.append(actor)
        db.commit()
    return {"message": "Actor added to favorites"} 