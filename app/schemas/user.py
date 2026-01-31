from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    """Payload para registro de usuario."""

    name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=50)
    phone: str | None = Field(None, max_length=50)
    country: str | None = Field(None, max_length=100)
    direction: str | None = Field(None, max_length=255)
    inversor: bool = False


class UserLogin(BaseModel):
    """Payload para login (email + contraseña)."""

    email: EmailStr
    password: str = Field(..., min_length=1)


class UserResponse(BaseModel):
    """Usuario devuelto en respuestas (sin contraseña)."""

    id: int
    name: str
    last_name: str
    email: str
    phone: str | None
    country: str | None
    direction: str | None
    inversor: bool

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    """Respuesta de login: usuario + token JWT."""

    access_token: str
    token_type: str = "bearer"
    user: UserResponse
