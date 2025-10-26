# Sadaka-Pass - Telegram Mini App для пожертвований

## 🕌 Описание проекта

Sadaka-Pass - это Telegram Mini App для сбора регулярных пожертвований (садака и садака-джария), разовых пожертвований на конкретные цели и калькулятор закята с функцией оплаты.

## 🏗️ Архитектура

### Backend (Python/FastAPI)
- **FastAPI** - основной фреймворк для API
- **SQLAlchemy** - ORM для работы с БД
- **Alembic** - миграции БД
- **Pydantic** - валидация данных
- **PostgreSQL** - основная база данных
- **Elasticsearch** - поиск фондов
- **Redis** - кэширование

### Frontend (React/TypeScript)
- **React 18** + **TypeScript**
- **Telegram WebApp SDK** - для Mini App
- **React Router** - навигация
- **Axios** - HTTP клиент

### Telegram Bot (Python/aiogram)
- **aiogram** - Telegram Bot API
- Интеграция с Mini App

## 🚀 Быстрый старт

### Предварительные требования
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Redis 6+
- Elasticsearch 8+

### Установка и запуск

1. **Клонирование репозитория**
```bash
git clone <repository-url>
cd sadaka-pass
```

2. **Backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

3. **Frontend**
```bash
cd frontend
npm install
npm start
```

4. **Telegram Bot**
```bash
cd telegram-bot
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## 📁 Структура проекта

```
sadaka-pass/
├── backend/                 # Python/FastAPI
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── core/           # Config, security
│   ├── migrations/         # Alembic migrations
│   ├── tests/              # pytest tests
│   └── requirements.txt
├── frontend/               # React/TypeScript
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Pages
│   │   ├── hooks/          # Custom hooks
│   │   ├── services/       # API services
│   │   └── types/          # TypeScript types
│   ├── public/             # Static assets
│   └── package.json
├── telegram-bot/           # Python/aiogram
├── docs/                   # Документация
├── docker-compose.yml      # Docker конфигурация
└── README.md
```

## 🔧 Конфигурация

### Переменные окружения

Создайте файл `.env` в корне проекта:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/sadaka_pass

# Redis
REDIS_URL=redis://localhost:6379

# Elasticsearch
ELASTICSEARCH_URL=http://localhost:9200

# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_WEBAPP_URL=https://your-domain.com

# Payment Systems
YOOKASSA_SHOP_ID=your_shop_id
YOOKASSA_SECRET_KEY=your_secret_key
CLOUDPAYMENTS_PUBLIC_ID=your_public_id
CLOUDPAYMENTS_API_SECRET=your_api_secret

# Security
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 🧪 Тестирование

### Backend тесты
```bash
cd backend
pytest
```

### Frontend тесты
```bash
cd frontend
npm test
```

## 📚 API Документация

После запуска backend сервера, документация доступна по адресу:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🐳 Docker

### Development
```bash
docker-compose up -d
```

### Production
```bash
# Используйте docker-compose.prod.yml для продакшн окружения
docker-compose -f docker-compose.prod.yml up -d
```

## 🚀 GitLab CI/CD

Проект использует GitLab CI/CD для автоматизации сборки, тестирования и развертывания.

### Настройка
1. Настройте CI/CD переменные в GitLab Settings → CI/CD → Variables
2. Создайте Docker Runner с Docker-in-Docker
3. Настройте SSH доступ к staging/production серверам

Подробная документация: [docs/GITLAB_CI_SETUP.md](docs/GITLAB_CI_SETUP.md)

### Pipeline Stages
- **Lint** - проверка качества кода
- **Test** - запуск тестов
- **Build** - сборка Docker образов
- **Deploy** - развертывание на staging/production

## 📞 Поддержка

Для вопросов и поддержки обращайтесь к команде разработки.

## 📄 Лицензия

Все права защищены.
