import logging
import logging.config
import os
import sys
from datetime import datetime
from typing import Dict, Any, Optional
import json
from pathlib import Path

class JSONFormatter(logging.Formatter):
    """JSON форматтер для логов"""
    
    def format(self, record):
        log_entry = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
            'thread': record.thread,
            'process': record.process
        }
        
        # Добавляем исключение, если есть
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)
        
        # Добавляем дополнительные поля
        if hasattr(record, 'request_id'):
            log_entry['request_id'] = record.request_id
        
        if hasattr(record, 'user_id'):
            log_entry['user_id'] = record.user_id
        
        if hasattr(record, 'extra_data'):
            log_entry['extra_data'] = record.extra_data
        
        return json.dumps(log_entry, ensure_ascii=False)

class ColoredFormatter(logging.Formatter):
    """Цветной форматтер для консоли"""
    
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }
    
    def format(self, record):
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset = self.COLORS['RESET']
        
        # Форматируем сообщение
        formatted = super().format(record)
        
        # Добавляем цвет
        return f"{color}{formatted}{reset}"

class StructuredLogger:
    """Структурированный логгер"""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self._setup_logger()
    
    def _setup_logger(self):
        """Настраивает логгер"""
        if not self.logger.handlers:
            # Консольный хендлер
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            console_formatter = ColoredFormatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)
            
            # Файловый хендлер для JSON логов
            log_dir = Path("logs")
            log_dir.mkdir(exist_ok=True)
            
            file_handler = logging.FileHandler(
                log_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log"
            )
            file_handler.setLevel(logging.DEBUG)
            file_formatter = JSONFormatter()
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
            
            # Хендлер для ошибок
            error_handler = logging.FileHandler(
                log_dir / f"errors_{datetime.now().strftime('%Y%m%d')}.log"
            )
            error_handler.setLevel(logging.ERROR)
            error_handler.setFormatter(file_formatter)
            self.logger.addHandler(error_handler)
    
    def debug(self, message: str, **kwargs):
        """Логирует DEBUG сообщение"""
        self._log(logging.DEBUG, message, **kwargs)
    
    def info(self, message: str, **kwargs):
        """Логирует INFO сообщение"""
        self._log(logging.INFO, message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Логирует WARNING сообщение"""
        self._log(logging.WARNING, message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Логирует ERROR сообщение"""
        self._log(logging.ERROR, message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        """Логирует CRITICAL сообщение"""
        self._log(logging.CRITICAL, message, **kwargs)
    
    def _log(self, level: int, message: str, **kwargs):
        """Внутренний метод для логирования"""
        extra = {}
        
        # Добавляем дополнительные поля
        if 'request_id' in kwargs:
            extra['request_id'] = kwargs.pop('request_id')
        
        if 'user_id' in kwargs:
            extra['user_id'] = kwargs.pop('user_id')
        
        if 'extra_data' in kwargs:
            extra['extra_data'] = kwargs.pop('extra_data')
        
        # Логируем с дополнительными полями
        self.logger.log(level, message, extra=extra if extra else None)

class APILogger:
    """Логгер для API запросов"""
    
    def __init__(self):
        self.logger = StructuredLogger('api')
    
    def log_request(self, method: str, path: str, request_id: str, user_id: Optional[int] = None):
        """Логирует входящий запрос"""
        self.logger.info(
            f"API Request: {method} {path}",
            request_id=request_id,
            user_id=user_id
        )
    
    def log_response(self, method: str, path: str, status_code: int, 
                    request_id: str, duration: float, user_id: Optional[int] = None):
        """Логирует ответ"""
        level = logging.INFO if status_code < 400 else logging.WARNING
        self.logger.logger.log(
            level,
            f"API Response: {method} {path} -> {status_code} ({duration:.3f}s)",
            extra={
                'request_id': request_id,
                'user_id': user_id,
                'extra_data': {
                    'method': method,
                    'path': path,
                    'status_code': status_code,
                    'duration': duration
                }
            }
        )
    
    def log_error(self, method: str, path: str, error: str, 
                 request_id: str, user_id: Optional[int] = None):
        """Логирует ошибку API"""
        self.logger.error(
            f"API Error: {method} {path} - {error}",
            request_id=request_id,
            user_id=user_id
        )

class BusinessLogger:
    """Логгер для бизнес-логики"""
    
    def __init__(self):
        self.logger = StructuredLogger('business')
    
    def log_donation(self, donation_id: int, user_id: int, amount: float, 
                    currency: str, fund_id: int, status: str):
        """Логирует пожертвование"""
        self.logger.info(
            f"Donation processed: {donation_id}",
            user_id=user_id,
            extra_data={
                'donation_id': donation_id,
                'amount': amount,
                'currency': currency,
                'fund_id': fund_id,
                'status': status
            }
        )
    
    def log_subscription(self, subscription_id: int, user_id: int, 
                        plan_id: int, status: str):
        """Логирует подписку"""
        self.logger.info(
            f"Subscription updated: {subscription_id}",
            user_id=user_id,
            extra_data={
                'subscription_id': subscription_id,
                'plan_id': plan_id,
                'status': status
            }
        )
    
    def log_campaign(self, campaign_id: int, user_id: int, action: str, **kwargs):
        """Логирует действия с кампанией"""
        self.logger.info(
            f"Campaign {action}: {campaign_id}",
            user_id=user_id,
            extra_data={
                'campaign_id': campaign_id,
                'action': action,
                **kwargs
            }
        )
    
    def log_zakat_calculation(self, calculation_id: int, user_id: int, 
                             amount: float, above_nisab: bool):
        """Логирует расчет закята"""
        self.logger.info(
            f"Zakat calculation: {calculation_id}",
            user_id=user_id,
            extra_data={
                'calculation_id': calculation_id,
                'amount': amount,
                'above_nisab': above_nisab
            }
        )

class SecurityLogger:
    """Логгер для событий безопасности"""
    
    def __init__(self):
        self.logger = StructuredLogger('security')
    
    def log_auth_failure(self, ip: str, user_agent: str, reason: str):
        """Логирует неудачную аутентификацию"""
        self.logger.warning(
            f"Authentication failure: {reason}",
            extra_data={
                'ip': ip,
                'user_agent': user_agent,
                'reason': reason,
                'event_type': 'auth_failure'
            }
        )
    
    def log_rate_limit_exceeded(self, ip: str, endpoint: str, limit: int):
        """Логирует превышение лимита запросов"""
        self.logger.warning(
            f"Rate limit exceeded: {endpoint}",
            extra_data={
                'ip': ip,
                'endpoint': endpoint,
                'limit': limit,
                'event_type': 'rate_limit_exceeded'
            }
        )
    
    def log_suspicious_activity(self, ip: str, activity: str, details: Dict[str, Any]):
        """Логирует подозрительную активность"""
        self.logger.warning(
            f"Suspicious activity: {activity}",
            extra_data={
                'ip': ip,
                'activity': activity,
                'details': details,
                'event_type': 'suspicious_activity'
            }
        )

class PerformanceLogger:
    """Логгер для производительности"""
    
    def __init__(self):
        self.logger = StructuredLogger('performance')
    
    def log_slow_query(self, query: str, duration: float, params: Dict[str, Any]):
        """Логирует медленные запросы к БД"""
        self.logger.warning(
            f"Slow database query: {duration:.3f}s",
            extra_data={
                'query': query,
                'duration': duration,
                'params': params,
                'event_type': 'slow_query'
            }
        )
    
    def log_cache_miss(self, key: str, operation: str):
        """Логирует промахи кэша"""
        self.logger.info(
            f"Cache miss: {key}",
            extra_data={
                'cache_key': key,
                'operation': operation,
                'event_type': 'cache_miss'
            }
        )
    
    def log_external_api_call(self, service: str, endpoint: str, 
                             duration: float, status_code: int):
        """Логирует вызовы внешних API"""
        level = logging.INFO if status_code < 400 else logging.WARNING
        self.logger.logger.log(
            level,
            f"External API call: {service} {endpoint} -> {status_code} ({duration:.3f}s)",
            extra={
                'extra_data': {
                    'service': service,
                    'endpoint': endpoint,
                    'duration': duration,
                    'status_code': status_code,
                    'event_type': 'external_api_call'
                }
            }
        )

# Глобальные экземпляры логгеров
api_logger = APILogger()
business_logger = BusinessLogger()
security_logger = SecurityLogger()
performance_logger = PerformanceLogger()

def get_logger(name: str) -> StructuredLogger:
    """Получает логгер по имени"""
    return StructuredLogger(name)

def setup_logging(debug: bool = False):
    """Настраивает систему логирования"""
    log_level = logging.DEBUG if debug else logging.INFO
    
    # Базовая конфигурация
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Настройка уровней для разных логгеров
    logging.getLogger('uvicorn').setLevel(logging.INFO)
    logging.getLogger('uvicorn.access').setLevel(logging.INFO)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    logging.getLogger('elasticsearch').setLevel(logging.WARNING)
    logging.getLogger('redis').setLevel(logging.WARNING)
    
    # Создаем директорию для логов
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    return True
