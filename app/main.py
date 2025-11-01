from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.api.routes import users as users_router

# Ensure tables exist (for simple setups; in prod use Alembic migrations)
# Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

ALLOWED_ORIGINS = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,   # set True only if you use cookies/auth headers
    allow_methods=["*"],      # or list specific methods
    allow_headers=["*"],      # or list specific headers
    # expose_headers=["Content-Disposition"],  # add if you need to read custom headers in JS
)

app.include_router(users_router.router, prefix="/users", tags=["users"])

@app.get("/healthz")
def health_check():
    return {"status": "ok"}
