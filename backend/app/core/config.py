from pydantic_settings import BaseSettings
from pydantic import Field, field_validator, ConfigDict
from typing import Optional, List
import os
from pathlib import Path

class Settings(BaseSettings):
    """Настройки приложения"""
    
    # Основные настройки
    app_name: str = Field(default="Sadaka-Pass API", description="Название приложения")
    app_version: str = Field(default="1.0.0", description="Версия приложения")
    debug: bool = Field(default=False, description="Режим отладки")
    environment: str = Field(default="production", description="Окружение")
    
    # Безопасность
    secret_key: str = Field(default="development-secret-key-change-in-production", description="Секретный ключ")
    access_token_expire_minutes: int = Field(default=30, description="Время жизни токена в минутах")
    algorithm: str = Field(default="HS256", description="Алгоритм шифрования")
    
    # База данных
    database_url: str = Field(default="postgresql://sadaka_user:sadaka_password@localhost:5432/sadaka_pass", description="URL базы данных")
    database_pool_size: int = Field(default=10, description="Размер пула подключений")
    database_max_overflow: int = Field(default=20, description="Максимальное переполнение пула")
    database_pool_timeout: int = Field(default=30, description="Таймаут пула подключений")
    
    # Redis
    redis_url: str = Field(default="redis://localhost:6379/0", description="URL Redis")
    redis_password: Optional[str] = Field(default=None, description="Пароль Redis")
    redis_db: int = Field(default=0, description="Номер базы данных Redis")
    redis_max_connections: int = Field(default=20, description="Максимальное количество подключений к Redis")
    
    # Elasticsearch
    elasticsearch_url: str = Field(default="http://localhost:9200", description="URL Elasticsearch")
    elasticsearch_username: Optional[str] = Field(default=None, description="Имя пользователя Elasticsearch")
    elasticsearch_password: Optional[str] = Field(default=None, description="Пароль Elasticsearch")
    elasticsearch_index_prefix: str = Field(default="sadaka_pass", description="Префикс индексов")
    
    # Telegram Bot
    telegram_bot_token: str = Field(default="development-token", description="Токен Telegram бота")
    telegram_webapp_url: str = Field(default="http://localhost:3000", description="URL Telegram WebApp")
    telegram_webhook_url: Optional[str] = Field(default=None, description="URL webhook для Telegram")
    
    # Платежные системы
    yookassa_shop_id: str = Field(default="development-shop-id", description="ID магазина YooKassa")
    yookassa_secret_key: str = Field(default="development-secret-key", description="Секретный ключ YooKassa")
    yookassa_webhook_url: Optional[str] = Field(default=None, description="URL webhook для YooKassa")
    
    cloudpayments_public_id: str = Field(default="development-public-id", description="Публичный ID CloudPayments")
    cloudpayments_api_secret: str = Field(default="development-api-secret", description="API секрет CloudPayments")
    cloudpayments_webhook_url: Optional[str] = Field(default=None, description="URL webhook для CloudPayments")
    
    # Внешние API
    bot_e_replika_api_url: str = Field(default="http://localhost:8000", description="URL API bot.e-replika.ru")
    bot_e_replika_api_token: str = Field(default="development-token", description="Токен API bot.e-replika.ru")
    
    # CORS
    allowed_origins: List[str] = Field(
        default=["https://t.me", "https://web.telegram.org"],
        description="Разрешенные источники для CORS"
    )
    
    # Rate Limiting
    rate_limit_requests: int = Field(default=100, description="Количество запросов для rate limiting")
    rate_limit_window: int = Field(default=60, description="Окно времени для rate limiting в секундах")
    
    # Логирование
    log_level: str = Field(default="INFO", description="Уровень логирования")
    log_format: str = Field(default="json", description="Формат логов (json/text)")
    log_file: Optional[str] = Field(default=None, description="Файл для логов")
    
    # Мониторинг
    enable_metrics: bool = Field(default=True, description="Включить метрики")
    metrics_port: int = Field(default=9090, description="Порт для метрик")
    enable_health_checks: bool = Field(default=True, description="Включить проверки здоровья")
    
    # Файлы и загрузки
    max_file_size: int = Field(default=10 * 1024 * 1024, description="Максимальный размер файла в байтах")
    allowed_file_types: List[str] = Field(
        default=["image/jpeg", "image/png", "image/gif", "application/pdf"],
        description="Разрешенные типы файлов"
    )
    upload_dir: str = Field(default="uploads", description="Директория для загрузок")
    
    # Email
    smtp_host: Optional[str] = Field(default=None, description="SMTP хост")
    smtp_port: int = Field(default=587, description="SMTP порт")
    smtp_username: Optional[str] = Field(default=None, description="SMTP имя пользователя")
    smtp_password: Optional[str] = Field(default=None, description="SMTP пароль")
    smtp_use_tls: bool = Field(default=True, description="Использовать TLS для SMTP")
    
    # Уведомления
    enable_notifications: bool = Field(default=True, description="Включить уведомления")
    notification_channels: List[str] = Field(
        default=["email", "telegram"],
        description="Каналы уведомлений"
    )
    
    # Кэширование
    cache_ttl_default: int = Field(default=300, description="TTL кэша по умолчанию в секундах")
    cache_ttl_user_data: int = Field(default=1800, description="TTL кэша пользовательских данных")
    cache_ttl_fund_data: int = Field(default=3600, description="TTL кэша данных фондов")
    cache_ttl_campaign_data: int = Field(default=1800, description="TTL кэша данных кампаний")
    
    # Безопасность дополнительная
    enable_csrf_protection: bool = Field(default=True, description="Включить защиту от CSRF")
    enable_xss_protection: bool = Field(default=True, description="Включить защиту от XSS")
    enable_content_security_policy: bool = Field(default=True, description="Включить CSP")
    
    # Производительность
    enable_compression: bool = Field(default=True, description="Включить сжатие ответов")
    compression_min_size: int = Field(default=1024, description="Минимальный размер для сжатия")
    enable_etag: bool = Field(default=True, description="Включить ETag")
    
    # Резервное копирование
    backup_enabled: bool = Field(default=False, description="Включить резервное копирование")
    backup_schedule: str = Field(default="0 2 * * *", description="Расписание резервного копирования")
    backup_retention_days: int = Field(default=30, description="Количество дней хранения резервных копий")
    
    @field_validator('environment')
    @classmethod
    def validate_environment(cls, v):
        """Валидирует окружение"""
        allowed_envs = ['development', 'staging', 'production', 'testing']
        if v not in allowed_envs:
            raise ValueError(f'Environment must be one of: {", ".join(allowed_envs)}')
        return v
    
    @field_validator('log_level')
    @classmethod
    def validate_log_level(cls, v):
        """Валидирует уровень логирования"""
        allowed_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in allowed_levels:
            raise ValueError(f'Log level must be one of: {", ".join(allowed_levels)}')
        return v.upper()
    
    @field_validator('log_format')
    @classmethod
    def validate_log_format(cls, v):
        """Валидирует формат логов"""
        allowed_formats = ['json', 'text']
        if v not in allowed_formats:
            raise ValueError(f'Log format must be one of: {", ".join(allowed_formats)}')
        return v
    
    @field_validator('allowed_file_types')
    @classmethod
    def validate_file_types(cls, v):
        """Валидирует типы файлов"""
        if not v:
            raise ValueError('At least one file type must be allowed')
        return v
    
    @field_validator('notification_channels')
    @classmethod
    def validate_notification_channels(cls, v):
        """Валидирует каналы уведомлений"""
        allowed_channels = ['email', 'telegram', 'sms', 'push']
        for channel in v:
            if channel not in allowed_channels:
                raise ValueError(f'Notification channel must be one of: {", ".join(allowed_channels)}')
        return v
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }

# Глобальный экземпляр настроек
settings = Settings()

def get_settings() -> Settings:
    """Получает настройки приложения"""
    return settings