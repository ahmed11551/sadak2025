from pydantic import BaseModel, validator, Field
from typing import Optional, List, Dict, Any, Union
from decimal import Decimal
from datetime import datetime, date
import re
import logging

logger = logging.getLogger(__name__)

class ValidationError(Exception):
    """Кастомное исключение для ошибок валидации"""
    pass

class BaseValidationMixin:
    """Базовый миксин для валидации"""
    
    @classmethod
    def validate_required_fields(cls, data: Dict[str, Any], required_fields: List[str]):
        """Проверяет наличие обязательных полей"""
        missing_fields = [field for field in required_fields if field not in data or data[field] is None]
        if missing_fields:
            raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")
    
    @classmethod
    def validate_field_length(cls, value: str, field_name: str, min_length: int = 0, max_length: int = None):
        """Проверяет длину поля"""
        if not isinstance(value, str):
            raise ValidationError(f"{field_name} must be a string")
        
        if len(value) < min_length:
            raise ValidationError(f"{field_name} must be at least {min_length} characters long")
        
        if max_length and len(value) > max_length:
            raise ValidationError(f"{field_name} must be no more than {max_length} characters long")


class UserValidationMixin(BaseValidationMixin):
    """Миксин для валидации пользователей"""
    
    @staticmethod
    def validate_telegram_id(telegram_id: int) -> int:
        """Валидирует Telegram ID"""
        if not isinstance(telegram_id, int) or telegram_id <= 0:
            raise ValidationError("Telegram ID must be a positive integer")
        
        if telegram_id > 2**63 - 1:  # Максимальное значение для int64
            raise ValidationError("Telegram ID is too large")
        
        return telegram_id
    
    @staticmethod
    def validate_username(username: Optional[str]) -> Optional[str]:
        """Валидирует username"""
        if username is None:
            return None
        
        if not isinstance(username, str):
            raise ValidationError("Username must be a string")
        
        # Telegram username правила
        if not re.match(r'^[a-zA-Z0-9_]{5,32}$', username):
            raise ValidationError("Username must be 5-32 characters long and contain only letters, numbers, and underscores")
        
        return username
    
    @staticmethod
    def validate_language_code(language_code: str) -> str:
        """Валидирует языковой код"""
        if not isinstance(language_code, str):
            raise ValidationError("Language code must be a string")
        
        # Поддерживаемые языки
        supported_languages = ['ru', 'en', 'ar', 'uz', 'kk', 'ky', 'tg']
        if language_code not in supported_languages:
            raise ValidationError(f"Unsupported language code. Supported: {', '.join(supported_languages)}")
        
        return language_code


class FundValidationMixin(BaseValidationMixin):
    """Миксин для валидации фондов"""
    
    @staticmethod
    def validate_fund_name(name: str) -> str:
        """Валидирует название фонда"""
        if not isinstance(name, str):
            raise ValidationError("Fund name must be a string")
        
        if len(name.strip()) < 2:
            raise ValidationError("Fund name must be at least 2 characters long")
        
        if len(name) > 255:
            raise ValidationError("Fund name must be no more than 255 characters long")
        
        # Проверяем на недопустимые символы
        if re.search(r'[<>"\']', name):
            raise ValidationError("Fund name contains invalid characters")
        
        return name.strip()
    
    @staticmethod
    def validate_country_code(country_code: str) -> str:
        """Валидирует код страны"""
        if not isinstance(country_code, str):
            raise ValidationError("Country code must be a string")
        
        if len(country_code) != 2:
            raise ValidationError("Country code must be exactly 2 characters")
        
        if not country_code.isupper():
            raise ValidationError("Country code must be uppercase")
        
        # Проверяем, что это валидный ISO код
        valid_codes = [
            'RU', 'US', 'GB', 'DE', 'FR', 'IT', 'ES', 'CA', 'AU', 'JP',
            'CN', 'IN', 'BR', 'MX', 'AR', 'CL', 'CO', 'PE', 'VE', 'UY',
            'KZ', 'UZ', 'KG', 'TJ', 'TM', 'AF', 'PK', 'BD', 'LK', 'NP',
            'BT', 'MV', 'IR', 'IQ', 'SA', 'AE', 'QA', 'KW', 'BH', 'OM',
            'YE', 'JO', 'LB', 'SY', 'IL', 'PS', 'TR', 'CY', 'GR', 'BG',
            'RO', 'MD', 'UA', 'BY', 'LT', 'LV', 'EE', 'PL', 'CZ', 'SK',
            'HU', 'SI', 'HR', 'BA', 'RS', 'ME', 'MK', 'AL', 'XK', 'MT'
        ]
        
        if country_code not in valid_codes:
            raise ValidationError(f"Invalid country code: {country_code}")
        
        return country_code
    
    @staticmethod
    def validate_purposes(purposes: Optional[List[str]]) -> Optional[List[str]]:
        """Валидирует цели фонда"""
        if purposes is None:
            return None
        
        if not isinstance(purposes, list):
            raise ValidationError("Purposes must be a list")
        
        valid_purposes = [
            'mosque', 'orphans', 'medical', 'education', 'food',
            'emergency', 'water', 'clothing', 'shelter', 'other'
        ]
        
        for purpose in purposes:
            if not isinstance(purpose, str):
                raise ValidationError("Each purpose must be a string")
            
            if purpose not in valid_purposes:
                raise ValidationError(f"Invalid purpose: {purpose}. Valid purposes: {', '.join(valid_purposes)}")
        
        return purposes
    
    @staticmethod
    def validate_website_url(url: Optional[str]) -> Optional[str]:
        """Валидирует URL веб-сайта"""
        if url is None:
            return None
        
        if not isinstance(url, str):
            raise ValidationError("Website URL must be a string")
        
        # Простая проверка URL
        url_pattern = re.compile(
            r'^https?://'  # http:// или https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # домен
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
            r'(?::\d+)?'  # порт
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        if not url_pattern.match(url):
            raise ValidationError("Invalid website URL format")
        
        return url


class DonationValidationMixin(BaseValidationMixin):
    """Миксин для валидации пожертвований"""
    
    @staticmethod
    def validate_amount(amount: Union[int, float, Decimal, str]) -> Decimal:
        """Валидирует сумму пожертвования"""
        try:
            amount_decimal = Decimal(str(amount))
        except (ValueError, TypeError):
            raise ValidationError("Amount must be a valid number")
        
        if amount_decimal <= 0:
            raise ValidationError("Amount must be greater than 0")
        
        if amount_decimal > Decimal('10000000'):  # 10 миллионов
            raise ValidationError("Amount is too large (maximum 10,000,000)")
        
        # Проверяем точность (максимум 2 знака после запятой)
        if amount_decimal.as_tuple().exponent < -2:
            raise ValidationError("Amount cannot have more than 2 decimal places")
        
        return amount_decimal
    
    @staticmethod
    def validate_currency(currency: str) -> str:
        """Валидирует валюту"""
        if not isinstance(currency, str):
            raise ValidationError("Currency must be a string")
        
        valid_currencies = ['RUB', 'USD', 'EUR', 'KZT', 'UZS', 'KGS', 'TJS', 'TMT']
        
        if currency not in valid_currencies:
            raise ValidationError(f"Unsupported currency: {currency}. Supported: {', '.join(valid_currencies)}")
        
        return currency
    
    @staticmethod
    def validate_payment_method(payment_method: str) -> str:
        """Валидирует способ оплаты"""
        if not isinstance(payment_method, str):
            raise ValidationError("Payment method must be a string")
        
        valid_methods = ['yookassa', 'cloudpayments', 'stripe', 'paypal']
        
        if payment_method not in valid_methods:
            raise ValidationError(f"Unsupported payment method: {payment_method}. Supported: {', '.join(valid_methods)}")
        
        return payment_method


class CampaignValidationMixin(BaseValidationMixin):
    """Миксин для валидации кампаний"""
    
    @staticmethod
    def validate_campaign_title(title: str) -> str:
        """Валидирует название кампании"""
        if not isinstance(title, str):
            raise ValidationError("Campaign title must be a string")
        
        if len(title.strip()) < 5:
            raise ValidationError("Campaign title must be at least 5 characters long")
        
        if len(title) > 255:
            raise ValidationError("Campaign title must be no more than 255 characters long")
        
        return title.strip()
    
    @staticmethod
    def validate_campaign_description(description: str) -> str:
        """Валидирует описание кампании"""
        if not isinstance(description, str):
            raise ValidationError("Campaign description must be a string")
        
        if len(description.strip()) < 20:
            raise ValidationError("Campaign description must be at least 20 characters long")
        
        if len(description) > 5000:
            raise ValidationError("Campaign description must be no more than 5000 characters long")
        
        return description.strip()
    
    @staticmethod
    def validate_campaign_category(category: str) -> str:
        """Валидирует категорию кампании"""
        if not isinstance(category, str):
            raise ValidationError("Campaign category must be a string")
        
        valid_categories = [
            'mosque', 'orphans', 'medical', 'education', 'food',
            'emergency', 'water', 'clothing', 'shelter', 'infrastructure',
            'environment', 'animals', 'other'
        ]
        
        if category not in valid_categories:
            raise ValidationError(f"Invalid campaign category: {category}. Valid categories: {', '.join(valid_categories)}")
        
        return category
    
    @staticmethod
    def validate_goal_amount(goal_amount: Union[int, float, Decimal, str]) -> Decimal:
        """Валидирует целевую сумму кампании"""
        try:
            amount_decimal = Decimal(str(goal_amount))
        except (ValueError, TypeError):
            raise ValidationError("Goal amount must be a valid number")
        
        if amount_decimal < Decimal('1000'):  # Минимум 1000
            raise ValidationError("Goal amount must be at least 1,000")
        
        if amount_decimal > Decimal('100000000'):  # Максимум 100 миллионов
            raise ValidationError("Goal amount is too large (maximum 100,000,000)")
        
        return amount_decimal
    
    @staticmethod
    def validate_end_date(end_date: Optional[Union[str, date]]) -> Optional[date]:
        """Валидирует дату окончания кампании"""
        if end_date is None:
            return None
        
        if isinstance(end_date, str):
            try:
                end_date = datetime.fromisoformat(end_date).date()
            except ValueError:
                raise ValidationError("Invalid end date format. Use YYYY-MM-DD")
        
        if not isinstance(end_date, date):
            raise ValidationError("End date must be a date")
        
        # Проверяем, что дата в будущем
        if end_date <= date.today():
            raise ValidationError("End date must be in the future")
        
        # Проверяем, что дата не слишком далеко в будущем (максимум 2 года)
        max_date = date.today().replace(year=date.today().year + 2)
        if end_date > max_date:
            raise ValidationError("End date cannot be more than 2 years in the future")
        
        return end_date


class ZakatValidationMixin(BaseValidationMixin):
    """Миксин для валидации закята"""
    
    @staticmethod
    def validate_zakat_amount(amount: Union[int, float, Decimal, str]) -> Decimal:
        """Валидирует сумму для расчета закята"""
        try:
            amount_decimal = Decimal(str(amount))
        except (ValueError, TypeError):
            raise ValidationError("Amount must be a valid number")
        
        if amount_decimal < 0:
            raise ValidationError("Amount cannot be negative")
        
        if amount_decimal > Decimal('1000000000'):  # 1 миллиард
            raise ValidationError("Amount is too large (maximum 1,000,000,000)")
        
        return amount_decimal
    
    @staticmethod
    def validate_nisab_amount(nisab_amount: Union[int, float, Decimal, str]) -> Decimal:
        """Валидирует размер нисаба"""
        try:
            nisab_decimal = Decimal(str(nisab_amount))
        except (ValueError, TypeError):
            raise ValidationError("Nisab amount must be a valid number")
        
        if nisab_decimal <= 0:
            raise ValidationError("Nisab amount must be greater than 0")
        
        return nisab_decimal


class PartnerValidationMixin(BaseValidationMixin):
    """Миксин для валидации партнеров"""
    
    @staticmethod
    def validate_organization_name(name: str) -> str:
        """Валидирует название организации"""
        if not isinstance(name, str):
            raise ValidationError("Organization name must be a string")
        
        if len(name.strip()) < 2:
            raise ValidationError("Organization name must be at least 2 characters long")
        
        if len(name) > 255:
            raise ValidationError("Organization name must be no more than 255 characters long")
        
        return name.strip()
    
    @staticmethod
    def validate_email(email: str) -> str:
        """Валидирует email"""
        if not isinstance(email, str):
            raise ValidationError("Email must be a string")
        
        email_pattern = re.compile(
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        )
        
        if not email_pattern.match(email):
            raise ValidationError("Invalid email format")
        
        if len(email) > 254:
            raise ValidationError("Email is too long")
        
        return email.lower().strip()
    
    @staticmethod
    def validate_phone(phone: Optional[str]) -> Optional[str]:
        """Валидирует номер телефона"""
        if phone is None:
            return None
        
        if not isinstance(phone, str):
            raise ValidationError("Phone must be a string")
        
        # Убираем все нецифровые символы кроме +
        cleaned_phone = re.sub(r'[^\d+]', '', phone)
        
        # Проверяем формат
        if not re.match(r'^\+?[1-9]\d{1,14}$', cleaned_phone):
            raise ValidationError("Invalid phone number format")
        
        return cleaned_phone


# Фабрика валидаторов
class ValidatorFactory:
    """Фабрика для создания валидаторов"""
    
    @staticmethod
    def create_user_validator():
        """Создает валидатор для пользователей"""
        return UserValidationMixin()
    
    @staticmethod
    def create_fund_validator():
        """Создает валидатор для фондов"""
        return FundValidationMixin()
    
    @staticmethod
    def create_donation_validator():
        """Создает валидатор для пожертвований"""
        return DonationValidationMixin()
    
    @staticmethod
    def create_campaign_validator():
        """Создает валидатор для кампаний"""
        return CampaignValidationMixin()
    
    @staticmethod
    def create_zakat_validator():
        """Создает валидатор для закята"""
        return ZakatValidationMixin()
    
    @staticmethod
    def create_partner_validator():
        """Создает валидатор для партнеров"""
        return PartnerValidationMixin()
