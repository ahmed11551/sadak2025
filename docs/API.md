# Sadaka-Pass API Documentation

## Обзор

Sadaka-Pass API предоставляет RESTful интерфейс для управления пожертвованиями, подписками, кампаниями и расчетом закята в Telegram Mini App.

**Base URL:** `https://api.sadaka-pass.com/api/v1`

## Аутентификация

API использует Telegram WebApp initData для аутентификации пользователей.

### Заголовки запросов

```http
Content-Type: application/json
Authorization: Bearer <telegram_init_data>
```

## Эндпоинты

### Пользователи

#### Создать пользователя
```http
POST /users/
```

**Тело запроса:**
```json
{
  "telegram_id": 123456789,
  "username": "username",
  "first_name": "Имя",
  "last_name": "Фамилия",
  "language_code": "ru"
}
```

**Ответ:**
```json
{
  "id": 1,
  "telegram_id": 123456789,
  "username": "username",
  "first_name": "Имя",
  "last_name": "Фамилия",
  "language_code": "ru",
  "is_premium": false,
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### Получить пользователя по Telegram ID
```http
GET /users/telegram/{telegram_id}
```

### Фонды

#### Получить список фондов
```http
GET /funds/
```

**Параметры запроса:**
- `country_code` (string, optional) - Код страны
- `verified_only` (boolean, optional) - Только верифицированные
- `purposes` (string, optional) - Цели через запятую
- `skip` (integer, optional) - Смещение
- `limit` (integer, optional) - Лимит

**Ответ:**
```json
[
  {
    "id": 1,
    "name": "Фонд помощи",
    "description": "Описание фонда",
    "country_code": "RU",
    "purposes": ["mosque", "orphans"],
    "verified": true,
    "active": true,
    "logo_url": "https://example.com/logo.png",
    "website": "https://example.com"
  }
]
```

#### Получить фонд по ID
```http
GET /funds/{fund_id}
```

### Пожертвования

#### Инициировать пожертвование
```http
POST /donations/init
```

**Тело запроса:**
```json
{
  "fund_id": 1,
  "amount": 1000,
  "currency": "RUB",
  "payment_method": "yookassa"
}
```

**Ответ:**
```json
{
  "donation_id": 1,
  "payment_url": "https://yookassa.ru/checkout/...",
  "status": "pending"
}
```

#### Проверить статус пожертвования
```http
GET /donations/{donation_id}/status
```

### Подписки

#### Создать подписку
```http
POST /subscriptions/init
```

**Тело запроса:**
```json
{
  "plan_id": 1,
  "fund_id": 1,
  "amount": 290,
  "currency": "RUB",
  "period": "1M",
  "payment_method": "yookassa"
}
```

#### Управление подпиской
```http
PATCH /subscriptions/{subscription_id}
```

**Тело запроса:**
```json
{
  "status": "paused"  // active, paused, cancelled
}
```

### Кампании

#### Получить список кампаний
```http
GET /campaigns/
```

**Параметры запроса:**
- `country` (string, optional) - Код страны
- `category` (string, optional) - Категория
- `status` (string, optional) - Статус (active, completed, pending)
- `skip` (integer, optional) - Смещение
- `limit` (integer, optional) - Лимит

#### Создать кампанию
```http
POST /campaigns/
```

**Тело запроса:**
```json
{
  "fund_id": 1,
  "title": "Строительство мечети",
  "description": "Описание кампании",
  "category": "mosque",
  "goal_amount": 1000000,
  "country_code": "RU",
  "end_date": "2024-12-31",
  "banner_url": "https://example.com/banner.jpg"
}
```

#### Пожертвовать в кампанию
```http
POST /campaigns/{campaign_id}/donate
```

### Закят

#### Рассчитать закят
```http
POST /zakat/calc
```

**Тело запроса:**
```json
{
  "cash_at_home": 100000,
  "bank_accounts": 500000,
  "stocks": 200000,
  "business_goods": 300000,
  "gold_silver": 150000,
  "investment_property": 400000,
  "other_income": 50000,
  "debts": 100000,
  "expenses": 20000
}
```

**Ответ:**
```json
{
  "total_assets": 1200000,
  "total_liabilities": 120000,
  "zakatable_amount": 1080000,
  "nisab_amount": 200000,
  "above_nisab": true,
  "zakat_amount": 27000,
  "zakat_rate": 2.5,
  "currency": "RUB"
}
```

#### Получить текущий нисаб
```http
GET /zakat/nisab
```

### Поиск

#### Поиск фондов
```http
GET /search/funds/search
```

**Параметры запроса:**
- `q` (string, optional) - Поисковый запрос
- `country_code` (string, optional) - Код страны
- `purposes` (string, optional) - Цели через запятую
- `verified_only` (boolean, optional) - Только верифицированные
- `size` (integer, optional) - Количество результатов (1-100)
- `from_` (integer, optional) - Смещение

#### Поиск кампаний
```http
GET /search/campaigns/search
```

**Параметры запроса:**
- `q` (string, optional) - Поисковый запрос
- `category` (string, optional) - Категория
- `country_code` (string, optional) - Код страны
- `status` (string, optional) - Статус
- `size` (integer, optional) - Количество результатов
- `from_` (integer, optional) - Смещение

### Партнеры

#### Получить список партнеров
```http
GET /partners/funds
```

#### Создать заявку на партнерство
```http
POST /partners/applications
```

**Тело запроса:**
```json
{
  "organization_name": "Название организации",
  "contact_person": "Контактное лицо",
  "email": "contact@example.com",
  "phone": "+1234567890",
  "website": "https://example.com",
  "description": "Описание организации",
  "purposes": ["mosque", "orphans"]
}
```

## Коды ошибок

| Код | Описание |
|-----|----------|
| 400 | Неверный запрос |
| 401 | Не авторизован |
| 403 | Доступ запрещен |
| 404 | Не найдено |
| 422 | Ошибка валидации |
| 500 | Внутренняя ошибка сервера |

## Примеры ошибок

```json
{
  "error": "Validation Error",
  "detail": "Поле 'amount' обязательно для заполнения"
}
```

## Rate Limiting

API имеет ограничения на количество запросов:
- **Обычные пользователи:** 100 запросов в минуту
- **Premium пользователи:** 500 запросов в минуту

При превышении лимита возвращается ошибка 429.

## Webhooks

### YooKassa Webhook
```http
POST /payments/webhook/yookassa
```

### CloudPayments Webhook
```http
POST /payments/webhook/cloudpayments
```

## SDK и библиотеки

### Python
```python
import requests

# Создание пожертвования
response = requests.post(
    "https://api.sadaka-pass.com/api/v1/donations/init",
    json={
        "fund_id": 1,
        "amount": 1000,
        "currency": "RUB",
        "payment_method": "yookassa"
    },
    headers={
        "Authorization": f"Bearer {telegram_init_data}"
    }
)
```

### JavaScript
```javascript
// Создание пожертвования
const response = await fetch('https://api.sadaka-pass.com/api/v1/donations/init', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${telegramInitData}`
  },
  body: JSON.stringify({
    fund_id: 1,
    amount: 1000,
    currency: 'RUB',
    payment_method: 'yookassa'
  })
});
```

## Changelog

### v1.0.0 (2024-01-01)
- Первоначальный релиз API
- Поддержка пожертвований и подписок
- Калькулятор закята
- Система кампаний
- Поиск через Elasticsearch
