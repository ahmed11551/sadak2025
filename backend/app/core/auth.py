import hashlib
import hmac
import json
import time
from typing import Optional, Dict, Any
from urllib.parse import parse_qsl
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, Request
import logging

logger = logging.getLogger(__name__)

class TelegramAuthError(Exception):
    """Ошибка аутентификации Telegram"""
    pass

class TelegramAuthService:
    """Сервис для аутентификации через Telegram WebApp"""
    
    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        self.security = HTTPBearer(auto_error=False)
    
    def verify_telegram_data(self, init_data: str) -> Dict[str, Any]:
        """
        Проверяет подлинность данных Telegram WebApp
        
        Args:
            init_data: Строка initData от Telegram WebApp
            
        Returns:
            Dict с данными пользователя
            
        Raises:
            TelegramAuthError: Если данные не прошли проверку
        """
        try:
            # Парсим данные
            parsed_data = dict(parse_qsl(init_data))
            
            # Извлекаем hash
            received_hash = parsed_data.pop('hash', '')
            if not received_hash:
                raise TelegramAuthError("Missing hash in init data")
            
            # Проверяем время (данные должны быть не старше 24 часов)
            auth_date = int(parsed_data.get('auth_date', 0))
            if time.time() - auth_date > 86400:  # 24 часа
                raise TelegramAuthError("Init data is too old")
            
            # Создаем строку для проверки подписи
            data_check_string = '\n'.join([
                f"{key}={value}" for key, value in sorted(parsed_data.items())
            ])
            
            # Создаем секретный ключ
            secret_key = hmac.new(
                b"WebAppData",
                self.bot_token.encode(),
                hashlib.sha256
            ).digest()
            
            # Вычисляем hash
            calculated_hash = hmac.new(
                secret_key,
                data_check_string.encode(),
                hashlib.sha256
            ).hexdigest()
            
            # Проверяем подпись
            if not hmac.compare_digest(calculated_hash, received_hash):
                raise TelegramAuthError("Invalid hash signature")
            
            # Парсим данные пользователя
            user_data = {}
            if 'user' in parsed_data:
                user_data = json.loads(parsed_data['user'])
            
            return {
                'user': user_data,
                'auth_date': auth_date,
                'query_id': parsed_data.get('query_id'),
                'chat_type': parsed_data.get('chat_type'),
                'chat_instance': parsed_data.get('chat_instance'),
                'start_param': parsed_data.get('start_param')
            }
            
        except (ValueError, KeyError, json.JSONDecodeError) as e:
            logger.error(f"Error parsing Telegram init data: {e}")
            raise TelegramAuthError("Invalid init data format")
        except Exception as e:
            logger.error(f"Unexpected error in Telegram auth: {e}")
            raise TelegramAuthError("Authentication failed")
    
    async def get_current_user(self, request: Request) -> Optional[Dict[str, Any]]:
        """
        Получает текущего пользователя из заголовков
        
        Args:
            request: FastAPI Request объект
            
        Returns:
            Dict с данными пользователя или None
        """
        try:
            # Получаем Authorization заголовок
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return None
            
            # Извлекаем init_data
            init_data = auth_header[7:]  # Убираем "Bearer "
            
            # Проверяем данные
            telegram_data = self.verify_telegram_data(init_data)
            
            return telegram_data.get('user')
            
        except TelegramAuthError as e:
            logger.warning(f"Telegram auth error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in get_current_user: {e}")
            return None


class AuthDependency:
    """Зависимость для аутентификации"""
    
    def __init__(self, auth_service: TelegramAuthService):
        self.auth_service = auth_service
    
    async def __call__(self, request: Request) -> Dict[str, Any]:
        """Получает аутентифицированного пользователя"""
        user = await self.auth_service.get_current_user(request)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        return user


class OptionalAuthDependency:
    """Опциональная зависимость для аутентификации"""
    
    def __init__(self, auth_service: TelegramAuthService):
        self.auth_service = auth_service
    
    async def __call__(self, request: Request) -> Optional[Dict[str, Any]]:
        """Получает пользователя, если он аутентифицирован"""
        return await self.auth_service.get_current_user(request)


def create_auth_dependencies(bot_token: str):
    """Создает зависимости для аутентификации"""
    auth_service = TelegramAuthService(bot_token)
    
    return {
        'require_auth': AuthDependency(auth_service),
        'optional_auth': OptionalAuthDependency(auth_service),
        'auth_service': auth_service
    }


# Утилиты для работы с пользователями
class UserUtils:
    """Утилиты для работы с пользователями"""
    
    @staticmethod
    def get_user_display_name(user_data: Dict[str, Any]) -> str:
        """Получает отображаемое имя пользователя"""
        first_name = user_data.get('first_name', '')
        last_name = user_data.get('last_name', '')
        
        if first_name and last_name:
            return f"{first_name} {last_name}"
        elif first_name:
            return first_name
        elif last_name:
            return last_name
        else:
            return user_data.get('username', 'Unknown User')
    
    @staticmethod
    def get_user_locale(user_data: Dict[str, Any]) -> str:
        """Получает локаль пользователя"""
        language_code = user_data.get('language_code', 'en')
        
        # Маппинг языковых кодов
        locale_mapping = {
            'ru': 'ru',
            'en': 'en',
            'ar': 'ar',
            'uz': 'uz',
            'kk': 'kk',
            'ky': 'ky',
            'tg': 'tg'
        }
        
        return locale_mapping.get(language_code, 'en')
    
    @staticmethod
    def is_premium_user(user_data: Dict[str, Any]) -> bool:
        """Проверяет, является ли пользователь Premium"""
        return user_data.get('is_premium', False)
    
    @staticmethod
    def get_user_id(user_data: Dict[str, Any]) -> int:
        """Получает ID пользователя"""
        return user_data.get('id', 0)


# Middleware для автоматической аутентификации
class AuthMiddleware:
    """Middleware для автоматической аутентификации"""
    
    def __init__(self, auth_service: TelegramAuthService):
        self.auth_service = auth_service
    
    async def __call__(self, request: Request, call_next):
        """Обрабатывает запрос и добавляет информацию о пользователе"""
        # Получаем пользователя
        user = await self.auth_service.get_current_user(request)
        
        # Добавляем в состояние запроса
        request.state.user = user
        request.state.is_authenticated = user is not None
        
        response = await call_next(request)
        return response


# Декораторы для проверки прав доступа
def require_premium(func):
    """Декоратор для проверки Premium статуса"""
    async def wrapper(*args, **kwargs):
        # Получаем пользователя из аргументов
        user = None
        for arg in args:
            if isinstance(arg, dict) and 'id' in arg:
                user = arg
                break
        
        if not user or not UserUtils.is_premium_user(user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Premium subscription required"
            )
        
        return await func(*args, **kwargs)
    
    return wrapper


def require_active_user(func):
    """Декоратор для проверки активности пользователя"""
    async def wrapper(*args, **kwargs):
        # Получаем пользователя из аргументов
        user = None
        for arg in args:
            if isinstance(arg, dict) and 'id' in arg:
                user = arg
                break
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required"
            )
        
        return await func(*args, **kwargs)
    
    return wrapper
