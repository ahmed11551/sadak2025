from fastapi import FastAPI, Depends, HTTPException, status, Response
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
import logging
import os

from .core.config import settings
from .core.database import get_db
from .core.exceptions import ErrorHandlers
from .core.auth import create_auth_dependencies
from .core.logging_config import setup_logging
from .core.metrics import (
    api_metrics, business_metrics, database_metrics,
    external_service_metrics, system_metrics, health_checker, metrics_exporter
)
from .middleware import (
    LoggingMiddleware,
    SecurityHeadersMiddleware,
    RateLimitMiddleware,
    CORSMiddleware as CustomCORSMiddleware,
    RequestValidationMiddleware
)
from .api import donations, subscriptions, zakat, funds, partners, users, campaigns, search, webhooks

# Настройка логирования
debug_mode = os.getenv("DEBUG", "false").lower() == "true"
setup_logging(debug=debug_mode)
logger = logging.getLogger(__name__)

# Создаем зависимости для аутентификации
auth_deps = create_auth_dependencies(settings.telegram_bot_token)

# Create FastAPI app
app = FastAPI(
    title="Sadaka-Pass API",
    description="Telegram Mini App для пожертвований и расчета закята",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    contact={
        "name": "Sadaka-Pass Support",
        "email": "support@sadaka-pass.com",
        "url": "https://sadaka-pass.com/support"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    }
)

# Регистрируем обработчики ошибок
ErrorHandlers.register_handlers(app)

# Middleware (порядок важен!)
app.add_middleware(LoggingMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestValidationMiddleware)
app.add_middleware(RateLimitMiddleware, calls=100, period=60)  # 100 запросов в минуту

# CORS middleware с настройками безопасности
allowed_origins = os.getenv("ALLOWED_ORIGINS", "https://t.me,https://web.telegram.org").split(",")
app.add_middleware(
    CustomCORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
    max_age=86400
)

# Security
security = HTTPBearer()

# Include routers
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(funds.router, prefix="/api/v1/funds", tags=["funds"])
app.include_router(donations.router, prefix="/api/v1/donations", tags=["donations"])
app.include_router(subscriptions.router, prefix="/api/v1/subscriptions", tags=["subscriptions"])
app.include_router(zakat.router, prefix="/api/v1/zakat", tags=["zakat"])
app.include_router(partners.router, prefix="/api/v1/partners", tags=["partners"])
app.include_router(campaigns.router, prefix="/api/v1/campaigns", tags=["campaigns"])
app.include_router(search.router, prefix="/api/v1/search", tags=["search"])
app.include_router(webhooks.router, prefix="/api/v1/webhooks", tags=["webhooks"])


@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {
        "message": "Sadaka-Pass API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Проверка здоровья системы"""
    try:
        # Проверяем подключение к БД
        db.execute(text("SELECT 1"))
        
        # Записываем метрики
        database_metrics.record_connection("success")
        
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "version": "1.0.0"
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        database_metrics.record_connection("error")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection failed: {str(e)}"
        )


@app.get("/metrics")
async def get_metrics():
    """Получение метрик в формате Prometheus"""
    try:
        metrics_data = metrics_exporter.export_prometheus()
        return Response(
            content=metrics_data,
            media_type="text/plain; version=0.0.4; charset=utf-8"
        )
    except Exception as e:
        logger.error(f"Error getting metrics: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get metrics"
        )


@app.get("/metrics/json")
async def get_metrics_json():
    """Получение метрик в формате JSON"""
    try:
        return metrics_exporter.export_json()
    except Exception as e:
        logger.error(f"Error getting metrics JSON: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get metrics"
        )


@app.get("/health/detailed")
async def detailed_health_check(db: Session = Depends(get_db)):
    """Детальная проверка здоровья системы"""
    try:
        # Регистрируем проверки здоровья
        async def check_database():
            db.execute(text("SELECT 1"))
            return True
        
        async def check_redis():
            # Здесь будет проверка Redis
            return True
        
        async def check_elasticsearch():
            # Здесь будет проверка Elasticsearch
            return True
        
        # Регистрируем проверки
        health_checker.register_check("database", check_database)
        health_checker.register_check("redis", check_redis)
        health_checker.register_check("elasticsearch", check_elasticsearch)
        
        # Запускаем проверки
        results = await health_checker.run_checks()
        overall_status = health_checker.get_overall_status()
        
        return {
            "status": overall_status,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "checks": results,
            "version": "1.0.0"
        }
        
    except Exception as e:
        logger.error(f"Detailed health check failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Health check failed: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
