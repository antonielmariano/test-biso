import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session
from typing import List

from app.models.actor import Actor
from app.models.genre import Genre
from app.models.movie import Movie
from app.models.rating import Rating
from app.models.user import User

class MovieRecommender:
    def __init__(self, db: Session):
        self.db = db

    def get_user_movie_matrix(self) -> tuple:
        ratings = self.db.query(Rating).all()
        users = self.db.query(User).all()
        movies = self.db.query(Movie).all()
        
        user_movie_matrix = np.zeros((len(users), len(movies)))
        
        user_ids = [user.id for user in users]
        movie_ids = [movie.id for movie in movies]
        
        for rating in ratings:
            if rating.user_id in user_ids and rating.movie_id in movie_ids:
                user_idx = user_ids.index(rating.user_id)
                movie_idx = movie_ids.index(rating.movie_id)
                user_movie_matrix[user_idx, movie_idx] = rating.score
            
        return user_movie_matrix, users, movies

    def get_movie_features(self) -> np.ndarray:
        movies = self.db.query(Movie).all()
        genres = self.db.query(Genre).all()
        actors = self.db.query(Actor).all()
        
        movie_features = np.zeros((len(movies), len(genres) + len(actors)))
        
        for i, movie in enumerate(movies):
            for j, genre in enumerate(genres):
                if genre in movie.genres:
                    movie_features[i, j] = 1
                    
            for j, actor in enumerate(actors):
                if actor in movie.actors:
                    movie_features[i, len(genres) + j] = 1
                    
        return movie_features

    def collaborative_filtering(self, user_id: int, n_recommendations: int = 5) -> List[Movie]:
        user_movie_matrix, users, movies = self.get_user_movie_matrix()
        
        if user_movie_matrix.shape[1] == 0:
            return []  
        try:
            user_idx = next(i for i, u in enumerate(users) if u.id == user_id)
        except StopIteration:
            return []
    
        user_similarity = cosine_similarity(user_movie_matrix)
        
        similar_users = user_similarity[user_idx].argsort()[::-1][1:6]
        
        user_ratings = user_movie_matrix[user_idx]
        recommendations = []
        
        for similar_user in similar_users:
            similar_user_ratings = user_movie_matrix[similar_user]
            for movie_idx in range(len(movies)):
                if user_ratings[movie_idx] == 0 and similar_user_ratings[movie_idx] > 0:
                    recommendations.append((movies[movie_idx], similar_user_ratings[movie_idx]))
                    
        recommendations.sort(key=lambda x: x[1], reverse=True)
        return [movie for movie, _ in recommendations[:n_recommendations]]

    def content_based_filtering(self, user_id: int, n_recommendations: int = 5) -> List[Movie]:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return []
            
        favorite_genres = set(genre.id for genre in user.favorite_genres)
        favorite_actors = set(actor.id for actor in user.favorite_actors)
        
        movies = self.db.query(Movie).all()
        
        movie_scores = []
        for movie in movies:
            score = 0
            movie_genres = set(genre.id for genre in movie.genres)
            genre_similarity = len(favorite_genres.intersection(movie_genres)) / len(favorite_genres) if favorite_genres else 0
            
            movie_actors = set(actor.id for actor in movie.actors)
            actor_similarity = len(favorite_actors.intersection(movie_actors)) / len(favorite_actors) if favorite_actors else 0
            
            score = 0.6 * genre_similarity + 0.4 * actor_similarity
            movie_scores.append((movie, score))
            
        movie_scores.sort(key=lambda x: x[1], reverse=True)
        return [movie for movie, _ in movie_scores[:n_recommendations]]

    def get_recommendations(self, user_id: int, n_recommendations: int = 5) -> List[Movie]:
        cf_recommendations = self.collaborative_filtering(user_id, n_recommendations)
        cb_recommendations = self.content_based_filtering(user_id, n_recommendations)
        
        all_recommendations = []
        seen = set()
        
        for movie in cb_recommendations + cf_recommendations:
            if movie.id not in seen:
                all_recommendations.append(movie)
                seen.add(movie.id)
            if len(all_recommendations) >= n_recommendations:
                break
    
        return all_recommendations