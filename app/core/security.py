"""
Lógica de seguridad (hashing/JWT) para el MVP.
Regla del proyecto: la lógica de auth/seguridad vive en app/core/security.py.
"""

import hashlib
from datetime import UTC, datetime, timedelta

import bcrypt
import jwt

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY

# Bcrypt solo acepta hasta 72 bytes. Pre-hasheamos con SHA256 y pasamos bytes truncados.
_BCRYPT_MAX_BYTES = 72


def _to_bcrypt_bytes(password: str) -> bytes:
    """Convierte la contraseña a bytes de máximo 72 para bcrypt (SHA256 hex = 64 bytes)."""
    digest = hashlib.sha256(password.encode("utf-8")).hexdigest()
    b = digest.encode("ascii")
    return b[: _BCRYPT_MAX_BYTES]


def get_password_hash(password: str) -> str:
    b = _to_bcrypt_bytes(password)
    return bcrypt.hashpw(b, bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    b = _to_bcrypt_bytes(plain_password)
    return bcrypt.checkpw(b, hashed_password.encode("utf-8"))


def create_access_token(subject: str | int) -> str:
    """Crea un JWT con sub=subject (p. ej. user id) y expiración."""
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(subject), "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
