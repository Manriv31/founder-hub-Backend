from fastapi import APIRouter

router = APIRouter()

# Importar endpoints
from app.api.v1.endpoints import auth, health

router.include_router(
    health.router,
    prefix="/health",
    tags=["Health"]
)
router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Auth"]
)

# Exportar router
api_router = router
