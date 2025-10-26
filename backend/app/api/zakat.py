from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from decimal import Decimal
from ..core.database import get_db
from ..models.models import ZakatCalculation, User
from ..schemas.schemas import ZakatCalculationCreate, ZakatCalculationUpdate, ZakatCalculation as ZakatSchema

router = APIRouter()

# Текущий нисаб (может обновляться)
CURRENT_NISAB = Decimal("952389")  # В рублях
ZAKAT_RATE = Decimal("0.025")  # 2.5%


@router.post("/calc", response_model=ZakatSchema)
async def calculate_zakat(
    zakat_data: ZakatCalculationCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Рассчитать закят"""
    # Проверяем существование пользователя
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Рассчитываем общую сумму активов
    total_assets = (
        zakat_data.cash_at_home +
        zakat_data.bank_accounts +
        zakat_data.shares_value +
        zakat_data.goods_profit +
        zakat_data.gold_silver_value +
        zakat_data.property_investments +
        zakat_data.other_income
    )
    
    # Рассчитываем общие обязательства
    total_liabilities = zakat_data.debts + zakat_data.expenses
    
    # Рассчитываем облагаемую закятом сумму
    zakatable_amount = total_assets - total_liabilities
    
    # Рассчитываем закят (только если сумма больше нисаба)
    zakat_amount = Decimal("0")
    if zakatable_amount > CURRENT_NISAB:
        zakat_amount = zakatable_amount * ZAKAT_RATE
    
    # Создаем или обновляем расчет
    existing_calc = db.query(ZakatCalculation).filter(
        ZakatCalculation.user_id == user_id
    ).first()
    
    if existing_calc:
        # Обновляем существующий расчет
        for field, value in zakat_data.dict().items():
            setattr(existing_calc, field, value)
        
        existing_calc.total_assets = total_assets
        existing_calc.total_liabilities = total_liabilities
        existing_calc.zakatable_amount = zakatable_amount
        existing_calc.nisab_amount = CURRENT_NISAB
        existing_calc.zakat_amount = zakat_amount
        
        db.commit()
        db.refresh(existing_calc)
        return existing_calc
    else:
        # Создаем новый расчет
        db_calc = ZakatCalculation(
            user_id=user_id,
            **zakat_data.dict(),
            total_assets=total_assets,
            total_liabilities=total_liabilities,
            zakatable_amount=zakatable_amount,
            nisab_amount=CURRENT_NISAB,
            zakat_amount=zakat_amount
        )
        
        db.add(db_calc)
        db.commit()
        db.refresh(db_calc)
        return db_calc


@router.post("/pay", response_model=dict)
async def pay_zakat(
    zakat_id: int,
    payment_method: str,
    db: Session = Depends(get_db)
):
    """Оплатить закят"""
    zakat_calc = db.query(ZakatCalculation).filter(ZakatCalculation.id == zakat_id).first()
    if not zakat_calc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Zakat calculation not found"
        )
    
    if zakat_calc.is_paid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Zakat already paid"
        )
    
    if zakat_calc.zakat_amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Zakat amount is zero or negative"
        )
    
    # Здесь должна быть логика создания платежа в платежной системе
    # Пока возвращаем mock данные
    payment_url = f"https://payment.example.com/zakat/{zakat_id}"
    
    return {
        "zakat_id": zakat_id,
        "amount": float(zakat_calc.zakat_amount),
        "currency": "RUB",
        "payment_url": payment_url,
        "status": "pending"
    }


@router.post("/{zakat_id}/confirm", response_model=dict)
async def confirm_zakat_payment(
    zakat_id: int,
    payment_data: dict,
    db: Session = Depends(get_db)
):
    """Подтвердить успешную оплату закята"""
    zakat_calc = db.query(ZakatCalculation).filter(ZakatCalculation.id == zakat_id).first()
    if not zakat_calc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Zakat calculation not found"
        )
    
    zakat_calc.is_paid = True
    zakat_calc.payment_id = payment_data.get("payment_id")
    
    db.commit()
    
    return {
        "message": "Zakat payment confirmed successfully",
        "zakat_id": zakat_id,
        "is_paid": True
    }


@router.get("/user/{user_id}", response_model=list)
async def get_user_zakat_history(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Получить историю расчетов закята пользователя"""
    calculations = db.query(ZakatCalculation).filter(
        ZakatCalculation.user_id == user_id
    ).order_by(ZakatCalculation.created_at.desc()).all()
    
    return [
        {
            "id": calc.id,
            "total_assets": float(calc.total_assets),
            "total_liabilities": float(calc.total_liabilities),
            "zakatable_amount": float(calc.zakatable_amount),
            "nisab_amount": float(calc.nisab_amount),
            "zakat_amount": float(calc.zakat_amount),
            "is_paid": calc.is_paid,
            "created_at": calc.created_at,
            "updated_at": calc.updated_at
        }
        for calc in calculations
    ]


@router.get("/nisab", response_model=dict)
async def get_current_nisab():
    """Получить текущий нисаб"""
    return {
        "nisab_amount": float(CURRENT_NISAB),
        "currency": "RUB",
        "zakat_rate": float(ZAKAT_RATE),
        "description": "Текущий нисаб для расчета закята"
    }
