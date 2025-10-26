# Sadaka-Pass - План развертывания

## 🎯 Рекомендуемая архитектура развертывания

### **Вариант 1: Docker + VPS (РЕКОМЕНДУЕМЫЙ)**

#### **Инфраструктура:**
```
┌─────────────────────────────────────────┐
│                VPS Server               │
│  ┌─────────────┐  ┌─────────────────┐   │
│  │   Nginx     │  │   Docker        │   │
│  │  (Reverse   │  │   Containers    │   │
│  │   Proxy)    │  │                 │   │
│  └─────────────┘  └─────────────────┘   │
│                                         │
│  ┌─────────────────────────────────────┐│
│  │        Docker Services              ││
│  │  • Backend (FastAPI)                ││
│  │  • Frontend (React)                 ││
│  │  • Admin Panel (React)              ││
│  │  • Telegram Bot                      ││
│  │  • PostgreSQL                       ││
│  │  • Redis                            ││
│  │  • Elasticsearch                    ││
│  └─────────────────────────────────────┘│
└─────────────────────────────────────────┘
```

#### **Требования к серверу:**
- **CPU:** 4 cores (минимум 2)
- **RAM:** 8GB (минимум 4GB)
- **SSD:** 100GB (минимум 50GB)
- **OS:** Ubuntu 20.04+ / CentOS 8+
- **Network:** 1Gbps

#### **Стоимость VPS:**
- **DigitalOcean:** $40-80/месяц
- **Linode:** $40-80/месяц  
- **Hetzner:** $20-50/месяц
- **Timeweb:** $30-60/месяц

---

## 📋 Что нужно от заказчика

### **1. Технические данные:**
- ✅ **Домен** для Telegram Bot и WebApp
- ✅ **Telegram Bot токен** (создается через @BotFather)
- ✅ **Ключи платежных систем:**
  - YooKassa: Shop ID + Secret Key
  - CloudPayments: Public ID + API Secret
- ✅ **API токен** для bot.e-replika.ru
- ✅ **Email настройки** для уведомлений (SMTP)

### **2. Контент:**
- ✅ **Список фондов** с описаниями и логотипами
- ✅ **Категории кампаний** и их описания
- ✅ **Политики** (конфиденциальности, пользовательское соглашение)
- ✅ **Переводы** на нужные языки (RU/EN/AR)

### **3. Юридические документы:**
- ✅ **Лицензии** на благотворительную деятельность
- ✅ **Соглашения** с фондами-партнерами
- ✅ **Политики обработки** персональных данных

---

## 🚀 План развертывания (7 дней)

### **День 1-2: Подготовка инфраструктуры**
- Настройка VPS сервера
- Установка Docker и Docker Compose
- Настройка домена и SSL
- Создание Telegram Bot

### **День 3-4: Развертывание приложения**
- Деплой всех сервисов
- Настройка базы данных
- Конфигурация Elasticsearch
- Настройка мониторинга

### **День 5-6: Интеграции**
- Подключение платежных систем
- Настройка webhook'ов
- Интеграция с bot.e-replika.ru
- Тестирование всех функций

### **День 7: Запуск**
- Финальное тестирование
- Наполнение контентом
- Запуск в продакшен
- Обучение администраторов

---

## 💰 Детальная стоимость

### **Единоразовые затраты:**
- **Развертывание:** $2,000-3,000
- **Настройка:** $1,000-1,500
- **Тестирование:** $500-1,000
- **Обучение:** $500-1,000
- **Итого:** $4,000-6,500

### **Ежемесячные затраты:**
- **VPS сервер:** $40-80
- **Домен:** $1-2
- **SSL сертификат:** $0 (Let's Encrypt)
- **Мониторинг:** $10-20
- **Резервное копирование:** $5-10
- **Итого:** $56-112/месяц

### **Дополнительные услуги:**
- **Техподдержка:** $200-500/месяц
- **Обновления:** $100-300/месяц
- **Мониторинг 24/7:** $300-800/месяц

---

## 🔧 Технические детали

### **Docker Compose конфигурация:**
```yaml
version: '3.8'
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - backend
      - frontend

  backend:
    build: ./backend
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/sadaka
      - REDIS_URL=redis://redis:6379
      - ELASTICSEARCH_URL=http://elasticsearch:9200
    depends_on:
      - db
      - redis
      - elasticsearch

  frontend:
    build: ./frontend
    environment:
      - REACT_APP_API_URL=https://api.yourdomain.com

  telegram-bot:
    build: ./telegram-bot
    environment:
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
      - API_URL=https://api.yourdomain.com

  db:
    image: postgres:14
    environment:
      - POSTGRES_DB=sadaka
      - POSTGRES_USER=sadaka_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

  elasticsearch:
    image: elasticsearch:8.11.1
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    volumes:
      - es_data:/usr/share/elasticsearch/data

volumes:
  postgres_data:
  redis_data:
  es_data:
```

### **Nginx конфигурация:**
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    location /api/ {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        proxy_pass http://frontend:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 📊 Мониторинг и безопасность

### **Мониторинг:**
- **Prometheus** - сбор метрик
- **Grafana** - визуализация
- **AlertManager** - уведомления
- **Uptime monitoring** - проверка доступности

### **Безопасность:**
- **SSL/TLS** - шифрование трафика
- **Firewall** - ограничение доступа
- **Fail2ban** - защита от брутфорса
- **Regular updates** - обновления безопасности
- **Backup** - ежедневные резервные копии

---

## 🎯 Альтернативные варианты

### **Вариант 2: Managed Kubernetes**
- **Стоимость:** $200-500/месяц
- **Сложность:** Высокая
- **Время развертывания:** 2-3 недели
- **Подходит для:** Больших проектов с высокой нагрузкой

### **Вариант 3: Cloud (AWS/GCP)**
- **Стоимость:** $300-1000/месяц
- **Сложность:** Очень высокая
- **Время развертывания:** 3-4 недели
- **Подходит для:** Enterprise проектов

---

## ✅ Рекомендация

**Для Sadaka-Pass рекомендую Docker + VPS потому что:**

1. **Соответствует ТЗ** - все требования выполняются
2. **Оптимальная стоимость** - $56-112/месяц vs $200-1000/месяц
3. **Быстрый запуск** - 7 дней vs 2-4 недели
4. **Простота управления** - понятно заказчику
5. **Легкое масштабирование** - при росте можно мигрировать

**При росте проекта** (1000+ пользователей) можно будет мигрировать на Kubernetes без переписывания кода.
