from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyRead, CompanyUpdate


router = APIRouter()


@router.post("/", response_model=CompanyRead, status_code=status.HTTP_201_CREATED)
def create_company(payload: CompanyCreate, db: Session = Depends(get_db)) -> Company:
    existing = db.execute(select(Company).where(Company.name == payload.name)).scalar_one_or_none()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe una company con ese name.",
        )

    company = Company(
        name=payload.name.strip(),
        description=payload.description,
        founders=payload.founders,
    )
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


@router.get("/{company_id}", response_model=CompanyRead)
def read_company(company_id: int, db: Session = Depends(get_db)) -> Company:
    company = db.get(Company, company_id)
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company no encontrada.")
    return company


@router.get("/", response_model=list[CompanyRead])
def list_companies(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
) -> list[Company]:
    limit = min(max(limit, 1), 200)
    skip = max(skip, 0)
    companies = db.execute(select(Company).offset(skip).limit(limit)).scalars().all()
    return list(companies)


@router.put("/{company_id}", response_model=CompanyRead)
def update_company(
    company_id: int,
    payload: CompanyUpdate,
    db: Session = Depends(get_db),
) -> Company:
    company = db.get(Company, company_id)
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company no encontrada.")

    if payload.name is not None:
        name = payload.name.strip()
        existing = db.execute(
            select(Company).where(Company.name == name, Company.id != company_id)
        ).scalar_one_or_none()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe una company con ese name.",
            )
        company.name = name

    if payload.description is not None:
        company.description = payload.description
    if payload.founders is not None:
        company.founders = payload.founders

    db.add(company)
    db.commit()
    db.refresh(company)
    return company


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(company_id: int, db: Session = Depends(get_db)) -> Response:
    company = db.get(Company, company_id)
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company no encontrada.")

    db.delete(company)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

