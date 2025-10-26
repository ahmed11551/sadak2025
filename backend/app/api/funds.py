from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..core.database import get_db
from ..models.models import Fund
from ..schemas.schemas import FundCreate, FundUpdate, Fund as FundSchema

router = APIRouter()


@router.get("/", response_model=List[FundSchema])
async def get_funds(
    country_code: Optional[str] = Query(None, description="Фильтр по стране"),
    purpose: Optional[str] = Query(None, description="Фильтр по цели"),
    verified_only: bool = Query(False, description="Только верифицированные фонды"),
    active_only: bool = Query(True, description="Только активные фонды"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Получить список фондов с фильтрацией"""
    query = db.query(Fund)
    
    if country_code:
        query = query.filter(Fund.country_code == country_code)
    
    if purpose:
        query = query.filter(Fund.purposes.contains([purpose]))
    
    if verified_only:
        query = query.filter(Fund.verified == True)
    
    if active_only:
        query = query.filter(Fund.active == True)
    
    funds = query.offset(offset).limit(limit).all()
    return funds


@router.get("/{fund_id}", response_model=FundSchema)
async def get_fund(fund_id: int, db: Session = Depends(get_db)):
    """Получить фонд по ID"""
    fund = db.query(Fund).filter(Fund.id == fund_id).first()
    if not fund:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fund not found"
        )
    return fund


@router.post("/", response_model=FundSchema)
async def create_fund(fund: FundCreate, db: Session = Depends(get_db)):
    """Создать новый фонд (только для админов)"""
    db_fund = Fund(**fund.dict())
    db.add(db_fund)
    db.commit()
    db.refresh(db_fund)
    return db_fund


@router.put("/{fund_id}", response_model=FundSchema)
async def update_fund(fund_id: int, fund_update: FundUpdate, db: Session = Depends(get_db)):
    """Обновить данные фонда (только для админов)"""
    fund = db.query(Fund).filter(Fund.id == fund_id).first()
    if not fund:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fund not found"
        )
    
    update_data = fund_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(fund, field, value)
    
    db.commit()
    db.refresh(fund)
    return fund


@router.get("/search/", response_model=List[FundSchema])
async def search_funds(
    q: str = Query(..., description="Поисковый запрос"),
    country_code: Optional[str] = Query(None),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Поиск фондов по названию и описанию"""
    query = db.query(Fund).filter(
        Fund.active == True,
        Fund.name.ilike(f"%{q}%")
    )
    
    if country_code:
        query = query.filter(Fund.country_code == country_code)
    
    funds = query.limit(limit).all()
    return funds
