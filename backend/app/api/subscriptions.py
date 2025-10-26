from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from decimal import Decimal
from datetime import datetime, timedelta
from ..core.database import get_db
from ..models.models import Subscription, User, Fund
from ..schemas.schemas import SubscriptionCreate, SubscriptionUpdate, Subscription as SubscriptionSchema

router = APIRouter()


@router.post("/init", response_model=dict)
async def init_subscription(subscription: SubscriptionCreate, db: Session = Depends(get_db)):
    """Инициализировать подписку на регулярные пожертвования"""
    # Проверяем существование пользователя и фонда
    user = db.query(User).filter(User.id == subscription.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    fund = db.query(Fund).filter(Fund.id == subscription.fund_id).first()
    if not fund:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fund not found"
        )
    
    # Рассчитываем дату следующего платежа
    next_payment_date = calculate_next_payment_date(subscription.frequency)
    
    # Создаем подписку
    db_subscription = Subscription(
        **subscription.dict(),
        next_payment_date=next_payment_date
    )
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    
    return {
        "subscription_id": db_subscription.id,
        "amount": float(db_subscription.amount),
        "currency": db_subscription.currency,
        "frequency": db_subscription.frequency,
        "next_payment_date": db_subscription.next_payment_date,
        "status": "active"
    }


@router.get("/{subscription_id}", response_model=SubscriptionSchema)
async def get_subscription(subscription_id: int, db: Session = Depends(get_db)):
    """Получить информацию о подписке"""
    subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found"
        )
    return subscription


@router.patch("/{subscription_id}", response_model=SubscriptionSchema)
async def update_subscription(
    subscription_id: int,
    subscription_update: SubscriptionUpdate,
    db: Session = Depends(get_db)
):
    """Обновить подписку"""
    subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found"
        )
    
    update_data = subscription_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(subscription, field, value)
    
    db.commit()
    db.refresh(subscription)
    return subscription


@router.post("/{subscription_id}/pause", response_model=dict)
async def pause_subscription(subscription_id: int, db: Session = Depends(get_db)):
    """Приостановить подписку"""
    subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found"
        )
    
    subscription.status = "paused"
    db.commit()
    
    return {
        "message": "Subscription paused successfully",
        "subscription_id": subscription.id,
        "status": subscription.status
    }


@router.post("/{subscription_id}/resume", response_model=dict)
async def resume_subscription(subscription_id: int, db: Session = Depends(get_db)):
    """Возобновить подписку"""
    subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found"
        )
    
    subscription.status = "active"
    subscription.next_payment_date = calculate_next_payment_date(subscription.frequency)
    db.commit()
    
    return {
        "message": "Subscription resumed successfully",
        "subscription_id": subscription.id,
        "status": subscription.status,
        "next_payment_date": subscription.next_payment_date
    }


@router.post("/{subscription_id}/cancel", response_model=dict)
async def cancel_subscription(subscription_id: int, db: Session = Depends(get_db)):
    """Отменить подписку"""
    subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found"
        )
    
    subscription.status = "cancelled"
    db.commit()
    
    return {
        "message": "Subscription cancelled successfully",
        "subscription_id": subscription.id,
        "status": subscription.status
    }


@router.get("/user/{user_id}", response_model=List[SubscriptionSchema])
async def get_user_subscriptions(
    user_id: int,
    status_filter: str = None,
    db: Session = Depends(get_db)
):
    """Получить подписки пользователя"""
    query = db.query(Subscription).filter(Subscription.user_id == user_id)
    
    if status_filter:
        query = query.filter(Subscription.status == status_filter)
    
    subscriptions = query.all()
    return subscriptions


def calculate_next_payment_date(frequency: str) -> datetime:
    """Рассчитать дату следующего платежа"""
    now = datetime.utcnow()
    
    if frequency == "daily":
        return now + timedelta(days=1)
    elif frequency == "weekly":
        return now + timedelta(weeks=1)
    elif frequency == "monthly":
        return now + timedelta(days=30)
    else:
        return now + timedelta(days=30)  # По умолчанию месячная
