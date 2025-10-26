import logging
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exceptions import SQLAlchemyError, IntegrityError
from pydantic import ValidationError
import traceback
from typing import Union

logger = logging.getLogger(__name__)

class CustomHTTPException(HTTPException):
    """Кастомное HTTP исключение с дополнительными полями"""
    
    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: str = None,
        field: str = None,
        context: dict = None
    ):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code
        self.field = field
        self.context = context or {}


async def http_exception_handler(request: Request, exc: HTTPException):
    """Обработчик HTTP исключений"""
    request_id = getattr(request.state, 'request_id', None)
    
    logger.warning(
        f"HTTP {exc.status_code}: {exc.detail} "
        f"(Request ID: {request_id}, Path: {request.url.path})"
    )
    
    response_data = {
        "error": "HTTP Error",
        "detail": exc.detail,
        "status_code": exc.status_code
    }
    
    if request_id:
        response_data["request_id"] = request_id
    
    # Добавляем дополнительные поля для кастомных исключений
    if isinstance(exc, CustomHTTPException):
        if exc.error_code:
            response_data["error_code"] = exc.error_code
        if exc.field:
            response_data["field"] = exc.field
        if exc.context:
            response_data["context"] = exc.context
    
    return JSONResponse(
        status_code=exc.status_code,
        content=response_data,
        headers={"X-Request-ID": request_id} if request_id else None
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Обработчик ошибок валидации Pydantic"""
    request_id = getattr(request.state, 'request_id', None)
    
    logger.warning(
        f"Validation error: {exc.errors()} "
        f"(Request ID: {request_id}, Path: {request.url.path})"
    )
    
    # Форматируем ошибки валидации
    formatted_errors = []
    for error in exc.errors():
        formatted_error = {
            "field": ".".join(str(x) for x in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        }
        formatted_errors.append(formatted_error)
    
    response_data = {
        "error": "Validation Error",
        "detail": "Request validation failed",
        "errors": formatted_errors
    }
    
    if request_id:
        response_data["request_id"] = request_id
    
    return JSONResponse(
        status_code=422,
        content=response_data,
        headers={"X-Request-ID": request_id} if request_id else None
    )


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """Обработчик ошибок SQLAlchemy"""
    request_id = getattr(request.state, 'request_id', None)
    
    logger.error(
        f"Database error: {str(exc)} "
        f"(Request ID: {request_id}, Path: {request.url.path})",
        exc_info=True
    )
    
    # Определяем тип ошибки и соответствующий статус код
    if isinstance(exc, IntegrityError):
        status_code = 409
        error_detail = "Database integrity constraint violation"
    else:
        status_code = 500
        error_detail = "Database operation failed"
    
    response_data = {
        "error": "Database Error",
        "detail": error_detail,
        "status_code": status_code
    }
    
    if request_id:
        response_data["request_id"] = request_id
    
    return JSONResponse(
        status_code=status_code,
        content=response_data,
        headers={"X-Request-ID": request_id} if request_id else None
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Обработчик общих исключений"""
    request_id = getattr(request.state, 'request_id', None)
    
    logger.error(
        f"Unhandled exception: {str(exc)} "
        f"(Request ID: {request_id}, Path: {request.url.path})",
        exc_info=True
    )
    
    # В продакшене не показываем детали исключения
    response_data = {
        "error": "Internal Server Error",
        "detail": "An unexpected error occurred",
        "status_code": 500
    }
    
    if request_id:
        response_data["request_id"] = request_id
    
    return JSONResponse(
        status_code=500,
        content=response_data,
        headers={"X-Request-ID": request_id} if request_id else None
    )


class ErrorHandlers:
    """Класс для регистрации обработчиков ошибок"""
    
    @staticmethod
    def register_handlers(app):
        """Регистрирует все обработчики ошибок в приложении"""
        
        # HTTP исключения
        app.add_exception_handler(HTTPException, http_exception_handler)
        app.add_exception_handler(StarletteHTTPException, http_exception_handler)
        
        # Ошибки валидации
        app.add_exception_handler(RequestValidationError, validation_exception_handler)
        app.add_exception_handler(ValidationError, validation_exception_handler)
        
        # Ошибки базы данных
        app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
        app.add_exception_handler(IntegrityError, sqlalchemy_exception_handler)
        
        # Общие исключения
        app.add_exception_handler(Exception, general_exception_handler)


# Предопределенные ошибки для API
class APIErrors:
    """Предопределенные ошибки API"""
    
    # Пользователи
    USER_NOT_FOUND = CustomHTTPException(
        status_code=404,
        detail="User not found",
        error_code="USER_NOT_FOUND"
    )
    
    USER_ALREADY_EXISTS = CustomHTTPException(
        status_code=409,
        detail="User already exists",
        error_code="USER_ALREADY_EXISTS"
    )
    
    # Фонды
    FUND_NOT_FOUND = CustomHTTPException(
        status_code=404,
        detail="Fund not found",
        error_code="FUND_NOT_FOUND"
    )
    
    FUND_INACTIVE = CustomHTTPException(
        status_code=400,
        detail="Fund is not active",
        error_code="FUND_INACTIVE"
    )
    
    # Пожертвования
    DONATION_NOT_FOUND = CustomHTTPException(
        status_code=404,
        detail="Donation not found",
        error_code="DONATION_NOT_FOUND"
    )
    
    DONATION_ALREADY_PROCESSED = CustomHTTPException(
        status_code=400,
        detail="Donation already processed",
        error_code="DONATION_ALREADY_PROCESSED"
    )
    
    INVALID_PAYMENT_METHOD = CustomHTTPException(
        status_code=400,
        detail="Invalid payment method",
        error_code="INVALID_PAYMENT_METHOD"
    )
    
    # Кампании
    CAMPAIGN_NOT_FOUND = CustomHTTPException(
        status_code=404,
        detail="Campaign not found",
        error_code="CAMPAIGN_NOT_FOUND"
    )
    
    CAMPAIGN_NOT_ACTIVE = CustomHTTPException(
        status_code=400,
        detail="Campaign is not active",
        error_code="CAMPAIGN_NOT_ACTIVE"
    )
    
    CAMPAIGN_GOAL_REACHED = CustomHTTPException(
        status_code=400,
        detail="Campaign goal already reached",
        error_code="CAMPAIGN_GOAL_REACHED"
    )
    
    # Подписки
    SUBSCRIPTION_NOT_FOUND = CustomHTTPException(
        status_code=404,
        detail="Subscription not found",
        error_code="SUBSCRIPTION_NOT_FOUND"
    )
    
    SUBSCRIPTION_ALREADY_ACTIVE = CustomHTTPException(
        status_code=400,
        detail="Subscription is already active",
        error_code="SUBSCRIPTION_ALREADY_ACTIVE"
    )
    
    # Закят
    INVALID_ZAKAT_CALCULATION = CustomHTTPException(
        status_code=400,
        detail="Invalid zakat calculation data",
        error_code="INVALID_ZAKAT_CALCULATION"
    )
    
    ZAKAT_BELOW_NISAB = CustomHTTPException(
        status_code=400,
        detail="Assets below nisab threshold",
        error_code="ZAKAT_BELOW_NISAB"
    )
    
    # Партнеры
    PARTNER_APPLICATION_NOT_FOUND = CustomHTTPException(
        status_code=404,
        detail="Partner application not found",
        error_code="PARTNER_APPLICATION_NOT_FOUND"
    )
    
    PARTNER_APPLICATION_ALREADY_EXISTS = CustomHTTPException(
        status_code=409,
        detail="Partner application already exists",
        error_code="PARTNER_APPLICATION_ALREADY_EXISTS"
    )
    
    # Аутентификация
    INVALID_TELEGRAM_DATA = CustomHTTPException(
        status_code=401,
        detail="Invalid Telegram init data",
        error_code="INVALID_TELEGRAM_DATA"
    )
    
    UNAUTHORIZED = CustomHTTPException(
        status_code=401,
        detail="Unauthorized access",
        error_code="UNAUTHORIZED"
    )
    
    # Поиск
    SEARCH_ERROR = CustomHTTPException(
        status_code=500,
        detail="Search service error",
        error_code="SEARCH_ERROR"
    )
    
    ELASTICSEARCH_UNAVAILABLE = CustomHTTPException(
        status_code=503,
        detail="Search service unavailable",
        error_code="ELASTICSEARCH_UNAVAILABLE"
    )
