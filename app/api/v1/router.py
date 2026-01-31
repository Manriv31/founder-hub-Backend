from fastapi import APIRouter

router = APIRouter()

# Importar endpoints
from app.api.v1.endpoints import health
from app.api.v1.endpoints import companies
from app.api.v1.endpoints import products

router.include_router(
    health.router,
    prefix="/health",
    tags=["Health"]
)

router.include_router(
    companies.router,
    prefix="/companies",
    tags=["Companies"],
)

router.include_router(
    products.router,
    prefix="/products",
    tags=["Products"],
)

# Exportar router
api_router = router
