from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..models.models import User, Fund, Donation
from ..schemas.schemas import UserCreate, UserUpdate, User as UserSchema

router = APIRouter()


@router.post("/", response_model=UserSchema)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Создать нового пользователя"""
    # Проверяем, существует ли пользователь с таким telegram_id
    existing_user = db.query(User).filter(User.telegram_id == user.telegram_id).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this telegram_id already exists"
        )
    
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/{user_id}", response_model=UserSchema)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Получить пользователя по ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.get("/telegram/{telegram_id}", response_model=UserSchema)
async def get_user_by_telegram_id(telegram_id: int, db: Session = Depends(get_db)):
    """Получить пользователя по Telegram ID"""
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.put("/{user_id}", response_model=UserSchema)
async def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    """Обновить данные пользователя"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    return user


@router.get("/{user_id}/donations", response_model=List[dict])
async def get_user_donations(user_id: int, db: Session = Depends(get_db)):
    """Получить пожертвования пользователя"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    donations = db.query(Donation).filter(Donation.user_id == user_id).all()
    return [
        {
            "id": donation.id,
            "amount": float(donation.amount),
            "currency": donation.currency,
            "purpose": donation.purpose,
            "status": donation.status,
            "created_at": donation.created_at,
            "fund_name": donation.fund.name
        }
        for donation in donations
    ]


@router.get("/{user_id}/subscriptions", response_model=List[dict])
async def get_user_subscriptions(user_id: int, db: Session = Depends(get_db)):
    """Получить подписки пользователя"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    subscriptions = db.query(User.subscriptions).filter(User.id == user_id).first()
    return [
        {
            "id": sub.id,
            "amount": float(sub.amount),
            "currency": sub.currency,
            "frequency": sub.frequency,
            "status": sub.status,
            "next_payment_date": sub.next_payment_date,
            "fund_name": sub.fund.name
        }
        for sub in subscriptions
    ]
