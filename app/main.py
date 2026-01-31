from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.database import Base, engine

# Importar modelos para registrar metadata (tablas) en Base
from app.models.user import User  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crea el archivo SQLite y las tablas definidas en modelos (MVP).
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="My API", version="1.0.0", lifespan=lifespan)

# Registrar routers
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "API is running"}
