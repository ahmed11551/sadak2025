# Sadaka-Pass - Техническая документация

## 📋 Обзор проекта

Sadaka-Pass — это универсальный модуль внутри Telegram Mini App MubarakWay, объединяющий:
- Единоразовые и регулярные пожертвования (садака, садака-джария)
- Целевые кампании пользователей (создание и участие)
- Каталог фондов-партнёров
- Калькулятор закята
- Система прозрачных отчётов и аналитики

## 🏗️ Архитектура системы

### Компоненты системы

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Telegram Bot  │    │   Telegram      │    │   Admin Panel   │
│   (aiogram)     │    │   Mini App      │    │   (React)       │
│                 │    │   (React/TS)    │    │                 │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────▼─────────────┐
                    │     Backend API           │
                    │   (Python/FastAPI)        │
                    └─────────────┬─────────────┘
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        │                         │                         │
┌───────▼───────┐    ┌────────────▼────────────┐    ┌──────▼──────┐
│  PostgreSQL   │    │     Elasticsearch        │    │    Redis    │
│   Database    │    │     (Search Engine)      │    │   (Cache)   │
└───────────────┘    └─────────────────────────┘    └─────────────┘
        │                         │                         │
        └─────────────────────────┼─────────────────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │   External Services       │
                    │  YooKassa, CloudPayments  │
                    │  bot.e-replika.ru API     │
                    └───────────────────────────┘
```

### Технологический стек

**Backend:**
- Python 3.11+
- FastAPI - веб-фреймворк
- SQLAlchemy - ORM
- Alembic - миграции БД
- Pydantic - валидация данных
- aiogram - Telegram Bot API

**Frontend:**
- React 18 + TypeScript
- Telegram WebApp SDK
- React Router - навигация
- Axios - HTTP клиент
- Styled Components - стилизация

**База данных:**
- PostgreSQL - основная БД
- Elasticsearch - поиск и фильтрация
- Redis - кэширование

**Платежные системы:**
- YooKassa (РФ)
- CloudPayments (международные)

## 📊 Модели данных

### Основные сущности

#### User (Пользователь)
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    telegram_id INTEGER UNIQUE NOT NULL,
    username VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    language_code VARCHAR(10) DEFAULT 'ru',
    locale VARCHAR(10) DEFAULT 'ru',
    timezone VARCHAR(50) DEFAULT 'UTC',
    madhab VARCHAR(50),
    is_premium BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);
```

#### Fund (Фонд)
```sql
CREATE TABLE funds (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    country_code VARCHAR(3) NOT NULL,
    purposes JSONB,
    logo_url VARCHAR(500),
    website_url VARCHAR(500),
    contact_info JSONB,
    verified BOOLEAN DEFAULT FALSE,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);
```

#### Campaign (Кампания)
```sql
CREATE TABLE campaigns (
    id SERIAL PRIMARY KEY,
    owner_id INTEGER REFERENCES users(id),
    fund_id INTEGER REFERENCES funds(id),
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(100) NOT NULL,
    goal_amount DECIMAL(10,2) NOT NULL,
    collected_amount DECIMAL(10,2) DEFAULT 0,
    country_code VARCHAR(3) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    end_date DATE,
    banner_url VARCHAR(500),
    participants_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);
```

#### SubscriptionPlan (Тарифный план)
```sql
CREATE TABLE subscription_plans (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    display_name VARCHAR(100) NOT NULL,
    description TEXT,
    price_monthly DECIMAL(10,2) NOT NULL,
    price_3months DECIMAL(10,2),
    price_6months DECIMAL(10,2),
    price_12months DECIMAL(10,2),
    charity_percentage DECIMAL(5,2) DEFAULT 0,
    features JSONB,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);
```

## 🔌 API Endpoints

### Основные группы эндпоинтов

#### Фонды
- `GET /api/v1/funds` - список фондов с фильтрацией
- `GET /api/v1/funds/{id}` - информация о фонде
- `POST /api/v1/funds` - создание фонда (админ)
- `PUT /api/v1/funds/{id}` - обновление фонда (админ)

#### Пожертвования
- `POST /api/v1/donations/init` - инициализация пожертвования
- `POST /api/v1/donations/{id}/confirm` - подтверждение платежа
- `GET /api/v1/donations/{id}` - информация о пожертвовании
- `GET /api/v1/donations/user/{user_id}` - история пользователя

#### Подписки
- `POST /api/v1/subscriptions/init` - создание подписки
- `GET /api/v1/subscriptions/{id}` - информация о подписке
- `PATCH /api/v1/subscriptions/{id}` - управление подпиской
- `POST /api/v1/subscriptions/{id}/pause` - приостановка
- `POST /api/v1/subscriptions/{id}/resume` - возобновление
- `POST /api/v1/subscriptions/{id}/cancel` - отмена

#### Кампании
- `GET /api/v1/campaigns` - список кампаний
- `GET /api/v1/campaigns/{id}` - информация о кампании
- `POST /api/v1/campaigns` - создание кампании
- `POST /api/v1/campaigns/{id}/donate` - пожертвование в кампанию
- `GET /api/v1/campaigns/{id}/donations` - пожертвования кампании
- `GET /api/v1/campaigns/{id}/report` - отчет по кампании

#### Закят
- `POST /api/v1/zakat/calc` - расчет закята
- `POST /api/v1/zakat/pay` - оплата закята
- `GET /api/v1/zakat/user/{user_id}` - история расчетов
- `GET /api/v1/zakat/nisab` - текущий нисаб

#### Партнеры
- `POST /api/v1/partners/applications` - подача заявки
- `GET /api/v1/partners/applications` - список заявок (админ)
- `PATCH /api/v1/partners/applications/{id}` - обновление заявки
- `POST /api/v1/partners/applications/{id}/approve` - одобрение
- `POST /api/v1/partners/applications/{id}/reject` - отклонение

## 💳 Платежная система

### Логика выбора провайдера

```python
def select_payment_provider(card_bin: str, country_code: str) -> str:
    """
    Выбор платежного провайдера на основе BIN карты и страны
    """
    # Российские карты
    if country_code == "RU" or card_bin.startswith(("4", "5")):
        return "yookassa"
    
    # Международные карты
    return "cloudpayments"
```

### Webhook обработка

```python
@app.post("/api/v1/webhooks/yookassa")
async def yookassa_webhook(request: Request):
    """Обработка webhook от YooKassa"""
    # Валидация подписи
    # Обновление статуса платежа
    # Уведомления пользователя

@app.post("/api/v1/webhooks/cloudpayments")
async def cloudpayments_webhook(request: Request):
    """Обработка webhook от CloudPayments"""
    # Аналогичная логика
```

## 🔍 Elasticsearch индексы

### Индекс фондов
```json
{
  "mappings": {
    "properties": {
      "id": {"type": "keyword"},
      "name": {
        "type": "text",
        "fields": {
          "keyword": {"type": "keyword"}
        }
      },
      "description": {"type": "text"},
      "country_code": {"type": "keyword"},
      "purposes": {"type": "keyword"},
      "verified": {"type": "boolean"},
      "active": {"type": "boolean"},
      "created_at": {"type": "date"}
    }
  }
}
```

### Поисковые запросы
```json
{
  "query": {
    "bool": {
      "must": [
        {"term": {"active": true}},
        {"term": {"verified": true}}
      ],
      "filter": [
        {"terms": {"country_code": ["RU", "KZ", "TR"]}},
        {"terms": {"purposes": ["mosque", "orphans", "medical"]}}
      ]
    }
  },
  "sort": [
    {"verified": {"order": "desc"}},
    {"_score": {"order": "desc"}}
  ]
}
```

## 📱 Telegram Bot интеграция

### Inline режим
```python
# Команды бота
/sadaqa - открыть вкладку "Пожертвовать"
/support - быстрые донаты
/zakat - калькулятор закята
/campaigns - список кампаний
/partners - каталог фондов

# Callback data примеры
donate:fund=123;sum=500
support:sum=1000
sub:plan=premium;period=P12M
campaign:join:456
zakat:calc
```

### WebApp интеграция
```javascript
// Инициализация Telegram WebApp
const tg = window.Telegram.WebApp;
tg.ready();
tg.expand();

// Отправка данных в бот
tg.sendData(JSON.stringify({
  type: 'donation_completed',
  amount: 1000,
  fund_id: 123
}));
```

## 🔒 Безопасность

### Аутентификация
- Проверка подписи Telegram WebApp initData
- JWT токены для API доступа
- Rate limiting (50 req/min per user)

### Валидация данных
- Pydantic схемы для всех входных данных
- SQL injection защита через SQLAlchemy
- XSS защита через валидацию

### Платежная безопасность
- HMAC валидация webhook'ов
- Хранение токенов в Vault
- Логирование без чувствительных данных

## 📊 Аналитика и отчетность

### События аналитики
```python
# Типы событий
EVENT_TYPES = [
    'donation_initiated',
    'donation_completed',
    'subscription_created',
    'subscription_cancelled',
    'campaign_created',
    'campaign_joined',
    'zakat_calculated',
    'partner_applied'
]
```

### Отчеты фондов
- Автоматическая интеграция через webhook
- Поддержка PDF, CSV, XLSX форматов
- Верификация отчетов администраторами
- Прозрачная отчетность для пользователей

## 🚀 Деплой и DevOps

### Docker конфигурация
```yaml
# docker-compose.yml
services:
  backend:
    build: ./backend
    ports: ["8000:8000"]
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/sadaka_pass
    depends_on: [postgres, redis, elasticsearch]
  
  frontend:
    build: ./frontend
    ports: ["3000:3000"]
    environment:
      - REACT_APP_API_URL=http://localhost:8000
```

### CI/CD Pipeline
```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: |
          cd backend && pytest
          cd frontend && npm test
```

## 📈 Мониторинг

### Логирование
- Structured logging в JSON формате
- Централизованные логи через ELK Stack
- Алерты на критические ошибки

### Метрики
- Prometheus для сбора метрик
- Grafana для визуализации
- Uptime мониторинг

### Ошибки
- Sentry для отслеживания ошибок
- Автоматические уведомления
- Трекинг производительности

## 🔧 Разработка

### Локальная разработка
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm start

# Telegram Bot
cd telegram-bot
python main.py
```

### Тестирование
```bash
# Backend тесты
cd backend
pytest

# Frontend тесты
cd frontend
npm test

# Интеграционные тесты
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

## 📚 Дополнительные ресурсы

- [OpenAPI документация](http://localhost:8000/docs)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Telegram WebApp](https://core.telegram.org/bots/webapps)
- [YooKassa API](https://yookassa.ru/developers/api)
- [CloudPayments API](https://developers.cloudpayments.ru/)
