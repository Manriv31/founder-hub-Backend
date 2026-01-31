import os


def _get_env(key: str, default: str) -> str:
    value = os.getenv(key)
    return value if value and value.strip() else default


# SQLite por defecto para desarrollo.
# Se puede sobreescribir con variable de entorno: DATABASE_URL
DATABASE_URL: str = _get_env("DATABASE_URL", "sqlite:///./founder_hub.db")

