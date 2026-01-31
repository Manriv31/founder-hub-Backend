from fastapi import APIRouter

router = APIRouter()

# Importar endpoints
<<<<<<< HEAD
from app.api.v1.endpoints import health
from app.api.v1.endpoints import companies
from app.api.v1.endpoints import products
=======
from app.api.v1.endpoints import auth, health
>>>>>>> develop

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
