from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from decimal import Decimal
from datetime import datetime, date
from ..core.database import get_db
from ..models.models import Campaign, CampaignDonation, User, Fund
from ..schemas.schemas import CampaignCreate, CampaignUpdate, Campaign as CampaignSchema

router = APIRouter()


@router.get("/", response_model=List[CampaignSchema])
async def get_campaigns(
    country_code: Optional[str] = Query(None, description="Фильтр по стране"),
    category: Optional[str] = Query(None, description="Фильтр по категории"),
    status: Optional[str] = Query("active", description="Фильтр по статусу"),
    sort_by: str = Query("created_at", description="Сортировка: created_at, goal_amount, collected_amount"),
    sort_order: str = Query("desc", description="Порядок: asc, desc"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Получить список кампаний с фильтрацией"""
    query = db.query(Campaign)
    
    if country_code:
        query = query.filter(Campaign.country_code == country_code)
    
    if category:
        query = query.filter(Campaign.category == category)
    
    if status:
        query = query.filter(Campaign.status == status)
    
    # Сортировка
    if sort_by == "goal_amount":
        order_column = Campaign.goal_amount
    elif sort_by == "collected_amount":
        order_column = Campaign.collected_amount
    else:
        order_column = Campaign.created_at
    
    if sort_order == "asc":
        query = query.order_by(order_column.asc())
    else:
        query = query.order_by(order_column.desc())
    
    campaigns = query.offset(offset).limit(limit).all()
    return campaigns


@router.get("/{campaign_id}", response_model=CampaignSchema)
async def get_campaign(campaign_id: int, db: Session = Depends(get_db)):
    """Получить кампанию по ID"""
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    return campaign


@router.post("/", response_model=CampaignSchema)
async def create_campaign(
    campaign: CampaignCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Создать новую кампанию"""
    # Проверяем существование пользователя
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Проверяем фонд, если указан
    if campaign.fund_id:
        fund = db.query(Fund).filter(Fund.id == campaign.fund_id).first()
        if not fund:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Fund not found"
            )
    
    db_campaign = Campaign(
        owner_id=user_id,
        **campaign.model_dump()
    )
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    return db_campaign


@router.patch("/{campaign_id}", response_model=CampaignSchema)
async def update_campaign(
    campaign_id: int,
    campaign_update: CampaignUpdate,
    db: Session = Depends(get_db)
):
    """Обновить кампанию (только для владельца или админа)"""
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    update_data = campaign_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(campaign, field, value)
    
    db.commit()
    db.refresh(campaign)
    return campaign


@router.post("/{campaign_id}/donate", response_model=dict)
async def donate_to_campaign(
    campaign_id: int,
    donation_data: dict,
    db: Session = Depends(get_db)
):
    """Сделать пожертвование в кампанию"""
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    if campaign.status != "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Campaign is not active"
        )
    
    # Проверяем пользователя
    user = db.query(User).filter(User.id == donation_data["user_id"]).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Создаем пожертвование
    db_donation = CampaignDonation(
        campaign_id=campaign_id,
        **donation_data
    )
    db.add(db_donation)
    
    # Обновляем статистику кампании
    campaign.collected_amount += Decimal(str(donation_data["amount"]))
    campaign.participants_count += 1
    
    # Проверяем, достигнута ли цель
    if campaign.collected_amount >= campaign.goal_amount:
        campaign.status = "completed"
    
    db.commit()
    
    return {
        "donation_id": db_donation.id,
        "amount": float(donation_data["amount"]),
        "currency": donation_data["currency"],
        "campaign_progress": float(campaign.collected_amount / campaign.goal_amount * 100),
        "status": "pending"
    }


@router.get("/{campaign_id}/donations", response_model=List[dict])
async def get_campaign_donations(
    campaign_id: int,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Получить пожертвования кампании"""
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    donations = db.query(CampaignDonation).filter(
        CampaignDonation.campaign_id == campaign_id
    ).offset(offset).limit(limit).all()
    
    return [
        {
            "id": donation.id,
            "amount": float(donation.amount),
            "currency": donation.currency,
            "status": donation.status,
            "created_at": donation.created_at,
            "user_name": f"{donation.user.first_name} {donation.user.last_name}".strip()
        }
        for donation in donations
    ]


@router.post("/{campaign_id}/complete", response_model=dict)
async def complete_campaign(
    campaign_id: int,
    db: Session = Depends(get_db)
):
    """Завершить кампанию (только для владельца или админа)"""
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    campaign.status = "completed"
    db.commit()
    
    return {
        "message": "Campaign completed successfully",
        "campaign_id": campaign_id,
        "total_collected": float(campaign.collected_amount),
        "participants": campaign.participants_count
    }


@router.get("/{campaign_id}/report", response_model=dict)
async def get_campaign_report(
    campaign_id: int,
    db: Session = Depends(get_db)
):
    """Получить отчет по кампании"""
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    total_donations = db.query(CampaignDonation).filter(
        CampaignDonation.campaign_id == campaign_id,
        CampaignDonation.status == "completed"
    ).count()
    
    return {
        "campaign_id": campaign_id,
        "title": campaign.title,
        "goal_amount": float(campaign.goal_amount),
        "collected_amount": float(campaign.collected_amount),
        "participants_count": campaign.participants_count,
        "total_donations": total_donations,
        "progress_percentage": float(campaign.collected_amount / campaign.goal_amount * 100),
        "status": campaign.status,
        "created_at": campaign.created_at,
        "end_date": campaign.end_date,
        "fund_name": campaign.fund.name if campaign.fund else None
    }
