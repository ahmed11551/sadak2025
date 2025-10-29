"""
Сервис для работы с CloudPayments
"""
import hashlib
import hmac
import json
import logging
from typing import Dict, Any, Optional
from decimal import Decimal

logger = logging.getLogger(__name__)


class CloudPaymentsService:
    """Сервис для интеграции с CloudPayments"""
    
    def __init__(self, public_id: str, api_secret: str):
        """
        Инициализация сервиса
        
        Args:
            public_id: Публичный ID для CloudPayments
            api_secret: API секрет для подписи запросов
        """
        self.public_id = public_id
        self.api_secret = api_secret
        
    def generate_signature(self, data: str) -> str:
        """
        Генерация подписи для данных
        
        Args:
            data: Строка данных для подписи
            
        Returns:
            Подпись в формате hex
        """
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            data.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return signature
    
    def create_payment_params(
        self,
        amount: Decimal,
        invoice_id: str,
        description: str,
        currency: str = "RUB",
        email: Optional[str] = None,
        account_id: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Создание параметров для виджета CloudPayments
        
        Args:
            amount: Сумма платежа
            invoice_id: Уникальный ID заказа
            description: Описание платежа
            currency: Валюта (RUB, USD, EUR)
            email: Email пользователя (опционально)
            account_id: ID аккаунта пользователя (опционально)
            **kwargs: Дополнительные параметры
            
        Returns:
            Словарь с параметрами для виджета
        """
        # Формируем данные для подписи
        params = {
            "Amount": float(amount),
            "Currency": currency,
            "InvoiceId": invoice_id,
            "Description": description,
        }
        
        if email:
            params["Email"] = email
            
        if account_id:
            params["AccountId"] = account_id
            
        # Добавляем дополнительные параметры
        params.update(kwargs)
        
        # Генерируем подпись
        data_string = f"{params['Amount']}{params['Currency']}{params['InvoiceId']}{params['Description']}"
        signature = self.generate_signature(data_string)
        
        return {
            "public_id": self.public_id,
            "amount": params["Amount"],
            "currency": params["Currency"],
            "invoice_id": params["InvoiceId"],
            "description": params["Description"],
            "signature": signature,
            "email": email,
            "account_id": account_id,
            **kwargs
        }
    
    def verify_webhook_signature(
        self,
        transaction_id: str,
        amount: float,
        currency: str,
        status: str,
        signature: str
    ) -> bool:
        """
        Проверка подписи webhook от CloudPayments
        
        Args:
            transaction_id: ID транзакции
            amount: Сумма
            currency: Валюта
            status: Статус платежа
            signature: Подпись из webhook
            
        Returns:
            True если подпись валидна, False - иначе
        """
        # Формируем строку для проверки подписи
        data_string = f"{transaction_id}{amount}{currency}{status}"
        expected_signature = hmac.new(
            self.api_secret.encode('utf-8'),
            data_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(expected_signature, signature)
    
    def get_payment_url(self) -> str:
        """
        Получение URL для виджета CloudPayments
        
        Returns:
            URL виджета
        """
        return "https://widget.cloudpayments.ru/payment"
    
    def parse_payment_status(self, status_code: str) -> str:
        """
        Преобразование статуса CloudPayments в внутренний статус
        
        Args:
            status_code: Код статуса от CloudPayments
            
        Returns:
            Внутренний статус (pending, completed, failed)
        """
        status_mapping = {
            "Completed": "completed",
            "Authorized": "pending",
            "Cancelled": "failed",
            "Declined": "failed",
            "Pending": "pending"
        }
        
        return status_mapping.get(status_code, "pending")
