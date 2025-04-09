from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.endpoints import movies, users, ratings, auth
from app.db.base import Base, engine
from app.db.migrations import run_migrations

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """
    Executa as migrações do banco de dados durante a inicialização da aplicação.
    """
    run_migrations()

# Include routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(movies.router, prefix=f"{settings.API_V1_STR}/movies", tags=["movies"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(ratings.router, prefix=f"{settings.API_V1_STR}/ratings", tags=["ratings"])

@app.get("/")
def root():
    return {
        "message": "Welcome to the Movie Recommender API",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    } 