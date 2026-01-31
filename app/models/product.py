from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    name: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    active_users: Mapped[int | None] = mapped_column(Integer, nullable=True)

    selling: Mapped[bool] = mapped_column(Boolean, default=False)
    seaking_inversion: Mapped[bool] = mapped_column(Boolean, default=False)
    publish: Mapped[bool] = mapped_column(Boolean, default=False)

    price: Mapped[float | None] = mapped_column(Float, nullable=True)

    # MVP: opcional hasta integrar auth. Queda listo para relación con users.
    founder_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)

    is_company: Mapped[bool] = mapped_column(Boolean, default=False)
    country: Mapped[str | None] = mapped_column(String(100), nullable=True)
    launch_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    publish_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

