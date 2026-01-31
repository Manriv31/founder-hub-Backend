import os
import secrets


def _get_env(key: str, default: str) -> str:
    value = os.getenv(key)
    return value if value and value.strip() else default


# SQLite por defecto para desarrollo.
# Se puede sobreescribir con variable de entorno: DATABASE_URL
DATABASE_URL: str = _get_env("DATABASE_URL", "sqlite:///./founder_hub.db")

# JWT: en producción usa una clave secreta fuerte (variable de entorno).
SECRET_KEY: str = _get_env("SECRET_KEY", secrets.token_urlsafe(32))
ALGORITHM: str = _get_env("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(_get_env("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

