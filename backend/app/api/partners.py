from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..models.models import PartnerApplication
from ..schemas.schemas import PartnerApplicationCreate, PartnerApplicationUpdate, PartnerApplication as PartnerSchema

router = APIRouter()


@router.post("/applications", response_model=PartnerSchema)
async def create_partner_application(
    application: PartnerApplicationCreate,
    db: Session = Depends(get_db)
):
    """Создать заявку на партнерство"""
    db_application = PartnerApplication(**application.dict())
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application


@router.get("/applications", response_model=List[PartnerSchema])
async def get_partner_applications(
    status_filter: str = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """Получить список заявок на партнерство (только для админов)"""
    query = db.query(PartnerApplication)
    
    if status_filter:
        query = query.filter(PartnerApplication.status == status_filter)
    
    applications = query.offset(offset).limit(limit).all()
    return applications


@router.get("/applications/{application_id}", response_model=PartnerSchema)
async def get_partner_application(
    application_id: int,
    db: Session = Depends(get_db)
):
    """Получить заявку на партнерство по ID"""
    application = db.query(PartnerApplication).filter(
        PartnerApplication.id == application_id
    ).first()
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Partner application not found"
        )
    
    return application


@router.patch("/applications/{application_id}", response_model=PartnerSchema)
async def update_partner_application(
    application_id: int,
    application_update: PartnerApplicationUpdate,
    reviewer_id: int,
    db: Session = Depends(get_db)
):
    """Обновить заявку на партнерство (только для админов)"""
    application = db.query(PartnerApplication).filter(
        PartnerApplication.id == application_id
    ).first()
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Partner application not found"
        )
    
    update_data = application_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(application, field, value)
    
    application.reviewed_by = reviewer_id
    
    db.commit()
    db.refresh(application)
    return application


@router.post("/applications/{application_id}/approve", response_model=dict)
async def approve_partner_application(
    application_id: int,
    reviewer_id: int,
    db: Session = Depends(get_db)
):
    """Одобрить заявку на партнерство"""
    application = db.query(PartnerApplication).filter(
        PartnerApplication.id == application_id
    ).first()
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Partner application not found"
        )
    
    application.status = "approved"
    application.reviewed_by = reviewer_id
    
    db.commit()
    
    return {
        "message": "Partner application approved successfully",
        "application_id": application_id,
        "status": "approved"
    }


@router.post("/applications/{application_id}/reject", response_model=dict)
async def reject_partner_application(
    application_id: int,
    reviewer_id: int,
    review_notes: str,
    db: Session = Depends(get_db)
):
    """Отклонить заявку на партнерство"""
    application = db.query(PartnerApplication).filter(
        PartnerApplication.id == application_id
    ).first()
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Partner application not found"
        )
    
    application.status = "rejected"
    application.reviewed_by = reviewer_id
    application.review_notes = review_notes
    
    db.commit()
    
    return {
        "message": "Partner application rejected",
        "application_id": application_id,
        "status": "rejected",
        "review_notes": review_notes
    }
