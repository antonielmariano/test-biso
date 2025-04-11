# Movie Recommender API

A FastAPI-based movie recommendation system that uses both collaborative filtering and content-based filtering to provide personalized movie recommendations to users.

## Features

- User management (registration, authentication)
- Movie management (CRUD operations)
- Rating system
- Personalized movie recommendations based on:
  - User ratings
  - Favorite genres
  - Favorite actors
  - Movie similarities

## Tech Stack

- Python 3.11
- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker & Docker Compose
- scikit-learn (for recommendation algorithms)

## Project Structure

```
.
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   │           ├── movies.py
│   │           ├── users.py
│   │           └── ratings.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── db/
│   │   └── base.py
│   ├── models/
│   │   └── models.py
│   ├── schemas/
│   │   └── schemas.py
│   ├── services/
│   │   └── recommender.py
│   └── main.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env
└── .env.example
```

## Getting Started

1. Clone the repository:
```bash
git clone <repository-url>
cd test biso
```

2. Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

3. Edit the `.env` file with your configuration:
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password_here
POSTGRES_SERVER=db
POSTGRES_PORT=5432
POSTGRES_DB=movie_recommender
DATABASE_URL=postgresql://postgres:your_password_here@db:5432/movie_recommender

# API Settings
PROJECT_NAME=Test Biso
VERSION=1.0.0
API_V1_STR=/api/v1

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

4. Build and start the containers:
```bash
docker-compose up --build
```

5. The API will be available at `http://localhost:8000`

6. Access the API documentation at:
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## Database Migrations

The project uses Alembic for database migrations. Here's how to work with migrations:

1. Create a new migration:
```bash
docker-compose exec web alembic revision --autogenerate -m "description of changes"
```

2. Apply migrations:
```bash
docker-compose exec web alembic upgrade head
```

3. Rollback migrations:
```bash
docker-compose exec web alembic downgrade -1  # Rollback one migration
docker-compose exec web alembic downgrade base  # Rollback all migrations
```

4. Check migration status:
```bash
docker-compose exec web alembic current  # Show current migration
docker-compose exec web alembic history  # Show migration history
```

Note: The migrations will be automatically applied when the application starts through the `run_migrations()` function in `app/db/migrations.py`.

## API Endpoints

### Movies
- `GET /api/v1/movies/` - List all movies
- `GET /api/v1/movies/{movie_id}` - Get movie details
- `POST /api/v1/movies/` - Create a new movie
- `GET /api/v1/movies/{user_id}/recommendations` - Get personalized movie recommendations

### Users
- `POST /api/v1/users/` - Create a new user
- `GET /api/v1/users/` - List all users
- `GET /api/v1/users/{user_id}` - Get user details
- `POST /api/v1/users/{user_id}/favorite-genres/{genre_id}` - Add favorite genre
- `POST /api/v1/users/{user_id}/favorite-actors/{actor_id}` - Add favorite actor

### Ratings
- `POST /api/v1/ratings/` - Create a new rating
- `GET /api/v1/ratings/user/{user_id}` - Get user's ratings
- `GET /api/v1/ratings/movie/{movie_id}` - Get movie's ratings
- `GET /api/v1/ratings/movie/{movie_id}/average` - Get movie's average rating

## Recommendation Algorithm

The system uses a hybrid approach combining:

1. Collaborative Filtering:
   - Based on user-movie rating matrix
   - Uses cosine similarity to find similar users
   - Recommends movies liked by similar users

2. Content-Based Filtering:
   - Based on movie features (genres, actors)
   - User preferences (favorite genres, actors)
   - Calculates similarity scores

The final recommendations are a combination of both approaches, weighted to provide the most relevant suggestions.

## Development

To run the application in development mode:

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file based on `.env.example` and configure it.

4. Run the application:
```bash
uvicorn app.main:app --reload
```

## Testing

To run the tests:
```bash
pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 