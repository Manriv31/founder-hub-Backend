import json

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import TokenResponse, UserLogin, UserRegister, UserResponse

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register(request: Request, db: Session = Depends(get_db)) -> User:
    """Registra un nuevo usuario. Acepta JSON o body como string con JSON (doble codificado)."""
    try:
        body_bytes = await request.body()
        body = json.loads(body_bytes.decode("utf-8"))
    except (ValueError, UnicodeDecodeError, json.JSONDecodeError):
        raise HTTPException(status_code=400, detail="Cuerpo de la petición no es JSON válido")
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except ValueError:
            raise HTTPException(status_code=400, detail="Cuerpo de la petición no es JSON válido")
    data = UserRegister.model_validate(body)

    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    user = User(
        name=data.name,
        last_name=data.last_name,
        email=data.email,
        phone=data.phone,
        country=data.country,
        direction=data.direction,
        inversor=data.inversor,
        password_hash=get_password_hash(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin, db: Session = Depends(get_db)) -> TokenResponse:
    """Login por email y contraseña. Devuelve usuario + JWT."""
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")
    access_token = create_access_token(subject=user.id)
    return TokenResponse(access_token=access_token, user=UserResponse.model_validate(user))
