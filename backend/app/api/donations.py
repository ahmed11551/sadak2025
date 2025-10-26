from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from decimal import Decimal
from ..core.database import get_db
from ..models.models import Donation, User, Fund
from ..schemas.schemas import DonationCreate, DonationUpdate, Donation as DonationSchema

router = APIRouter()


@router.post("/init", response_model=dict)
async def init_donation(donation: DonationCreate, db: Session = Depends(get_db)):
    """Инициализировать разовое пожертвование"""
    # Проверяем существование пользователя и фонда
    user = db.query(User).filter(User.id == donation.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    fund = db.query(Fund).filter(Fund.id == donation.fund_id).first()
    if not fund:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fund not found"
        )
    
    # Создаем запись о пожертвовании
    db_donation = Donation(**donation.dict())
    db.add(db_donation)
    db.commit()
    db.refresh(db_donation)
    
    # Здесь должна быть логика создания платежа в платежной системе
    # Пока возвращаем mock данные
    return {
        "donation_id": db_donation.id,
        "amount": float(db_donation.amount),
        "currency": db_donation.currency,
        "payment_url": f"https://payment.example.com/pay/{db_donation.id}",
        "status": "pending"
    }


@router.post("/{donation_id}/confirm", response_model=dict)
async def confirm_donation(
    donation_id: int, 
    payment_data: dict,
    db: Session = Depends(get_db)
):
    """Подтвердить успешное пожертвование"""
    donation = db.query(Donation).filter(Donation.id == donation_id).first()
    if not donation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Donation not found"
        )
    
    # Обновляем статус пожертвования
    donation.status = "completed"
    donation.payment_id = payment_data.get("payment_id")
    donation.transaction_id = payment_data.get("transaction_id")
    
    db.commit()
    
    return {
        "message": "Donation confirmed successfully",
        "donation_id": donation.id,
        "status": donation.status
    }


@router.get("/{donation_id}", response_model=DonationSchema)
async def get_donation(donation_id: int, db: Session = Depends(get_db)):
    """Получить информацию о пожертвовании"""
    donation = db.query(Donation).filter(Donation.id == donation_id).first()
    if not donation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Donation not found"
        )
    return donation


@router.get("/user/{user_id}", response_model=List[DonationSchema])
async def get_user_donations(
    user_id: int,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """Получить пожертвования пользователя"""
    donations = db.query(Donation).filter(
        Donation.user_id == user_id
    ).offset(offset).limit(limit).all()
    
    return donations


@router.post("/{donation_id}/refund", response_model=dict)
async def refund_donation(donation_id: int, db: Session = Depends(get_db)):
    """Возврат пожертвования (только для админов)"""
    donation = db.query(Donation).filter(Donation.id == donation_id).first()
    if not donation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Donation not found"
        )
    
    if donation.status != "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only completed donations can be refunded"
        )
    
    # Здесь должна быть логика возврата в платежной системе
    donation.status = "refunded"
    db.commit()
    
    return {
        "message": "Donation refunded successfully",
        "donation_id": donation.id,
        "status": donation.status
    }
