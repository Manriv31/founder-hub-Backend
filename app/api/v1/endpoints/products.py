from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate


router = APIRouter()


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)) -> Product:
    existing = db.execute(select(Product).where(Product.name == payload.name)).scalar_one_or_none()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un product con ese name.",
        )

    product = Product(
        name=payload.name.strip(),
        description=payload.description,
        active_users=payload.active_users,
        selling=payload.selling,
        seaking_inversion=payload.seaking_inversion,
        publish=payload.publish,
        price=payload.price,
        founder_id=payload.founder_id,
        is_company=payload.is_company,
        country=payload.country,
        launch_date=payload.launch_date,
        publish_date=payload.publish_date,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get("/{product_id}", response_model=ProductRead)
def read_product(product_id: int, db: Session = Depends(get_db)) -> Product:
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product no encontrado.")
    return product


@router.get("/", response_model=list[ProductRead])
def list_products(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
) -> list[Product]:
    limit = min(max(limit, 1), 200)
    skip = max(skip, 0)
    products = db.execute(select(Product).offset(skip).limit(limit)).scalars().all()
    return list(products)


@router.put("/{product_id}", response_model=ProductRead)
def update_product(product_id: int, payload: ProductUpdate, db: Session = Depends(get_db)) -> Product:
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product no encontrado.")

    if payload.name is not None:
        name = payload.name.strip()
        existing = db.execute(
            select(Product).where(Product.name == name, Product.id != product_id)
        ).scalar_one_or_none()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe un product con ese name.",
            )
        product.name = name

    if payload.description is not None:
        product.description = payload.description

    if payload.active_users is not None:
        product.active_users = payload.active_users

    if payload.selling is not None:
        product.selling = payload.selling
    if payload.seaking_inversion is not None:
        product.seaking_inversion = payload.seaking_inversion
    if payload.publish is not None:
        product.publish = payload.publish

    if payload.price is not None:
        product.price = payload.price

    if payload.founder_id is not None:
        product.founder_id = payload.founder_id

    if payload.is_company is not None:
        product.is_company = payload.is_company
    if payload.country is not None:
        product.country = payload.country
    if payload.launch_date is not None:
        product.launch_date = payload.launch_date
    if payload.publish_date is not None:
        product.publish_date = payload.publish_date

    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)) -> Response:
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product no encontrado.")

    db.delete(product)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

