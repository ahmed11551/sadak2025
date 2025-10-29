"""
Webhook endpoints для обработки уведомлений от платежных систем
"""
from fastapi import APIRouter, Request, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any
import logging

from ..core.database import get_db
from ..core.config import settings
from ..services.cloudpayments_service import CloudPaymentsService
from ..models.models import Donation

logger = logging.getLogger(__name__)

router = APIRouter()

# Инициализируем сервис CloudPayments (пока с дефолтными значениями)
cloudpayments_service = CloudPaymentsService(
    public_id=settings.cloudpayments_public_id,
    api_secret=settings.cloudpayments_api_secret
)


@router.post("/cloudpayments")
async def cloudpayments_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Webhook для обработки уведомлений от CloudPayments
    
    CloudPayments будет отправлять POST запросы на этот endpoint
    для уведомления о статусе платежей.
    """
    try:
        # Получаем данные из webhook
        webhook_data = await request.json()
        logger.info(f"Received CloudPayments webhook: {webhook_data}")
        
        # Извлекаем основные поля
        transaction_id = webhook_data.get("TransactionId")
        invoice_id = webhook_data.get("InvoiceId")  # Это наш donation_id
        status_code = webhook_data.get("Status")
        amount = webhook_data.get("Amount")
        currency = webhook_data.get("Currency")
        signature = webhook_data.get("Signature")
        
        # Проверяем подпись
        if not cloudpayments_service.verify_webhook_signature(
            transaction_id=str(transaction_id),
            amount=float(amount),
            currency=currency,
            status=status_code,
            signature=signature
        ):
            logger.error(f"Invalid signature for transaction {transaction_id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid signature"
            )
        
        # Находим пожертвование
        if invoice_id:
            donation = db.query(Donation).filter(Donation.id == int(invoice_id)).first()
            
            if donation:
                # Обновляем статус пожертвования
                donation.payment_id = str(transaction_id)
                donation.status = cloudpayments_service.parse_payment_status(status_code)
                
                db.commit()
                db.refresh(donation)
                
                logger.info(f"Updated donation {donation.id} with status {donation.status}")
            else:
                logger.warning(f"Donation with ID {invoice_id} not found")
        else:
            logger.warning("No invoice_id in webhook data")
        
        # CloudPayments ожидает ответ в определенном формате
        return {
            "code": 0,  # 0 = успех
            "message": "OK"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing CloudPayments webhook: {str(e)}")
        # Возвращаем ошибку CloudPayments
        return {
            "code": 1,
            "message": "Internal server error"
        }


@router.get("/cloudpayments/test")
async def test_cloudpayments_webhook():
    """
    Тестовый endpoint для проверки webhook
    """
    return {
        "message": "CloudPayments webhook endpoint is working",
        "public_id": settings.cloudpayments_public_id,
        "widget_url": cloudpayments_service.get_payment_url()
    }


@router.post("/cloudpayments/test")
async def test_cloudpayments_webhook_post(request: Request):
    """
    Тестовый POST endpoint для проверки формата webhook
    """
    try:
        webhook_data = await request.json()
        return {
            "message": "Webhook received",
            "data": webhook_data
        }
    except Exception as e:
        return {
            "error": str(e)
        }
