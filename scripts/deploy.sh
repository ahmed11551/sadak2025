#!/bin/bash

# Sadaka-Pass - Автоматический скрипт развертывания
# Использование: ./deploy.sh [staging|production]

set -e

ENVIRONMENT=${1:-staging}
PROJECT_NAME="sadaka-pass"
DOMAIN=${2:-"yourdomain.com"}
EMAIL=${3:-"admin@yourdomain.com"}

echo "🚀 Начинаем развертывание Sadaka-Pass в окружение: $ENVIRONMENT"
echo "🌐 Домен: $DOMAIN"
echo "📧 Email: $EMAIL"

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для логирования
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
    exit 1
}

# Проверка прав root
if [[ $EUID -ne 0 ]]; then
   error "Этот скрипт должен быть запущен с правами root"
fi

# Проверка операционной системы
if ! command -v apt-get &> /dev/null; then
    error "Этот скрипт поддерживает только Ubuntu/Debian"
fi

log "Обновляем систему..."
apt update && apt upgrade -y

log "Устанавливаем необходимые пакеты..."
apt install -y curl wget git unzip software-properties-common apt-transport-https ca-certificates gnupg lsb-release

# Установка Docker
if ! command -v docker &> /dev/null; then
    log "Устанавливаем Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
    
    # Добавляем пользователя в группу docker
    usermod -aG docker $USER
    
    # Включаем автозапуск Docker
    systemctl enable docker
    systemctl start docker
else
    log "Docker уже установлен"
fi

# Установка Docker Compose
if ! command -v docker-compose &> /dev/null; then
    log "Устанавливаем Docker Compose..."
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
else
    log "Docker Compose уже установлен"
fi

# Установка Nginx
if ! command -v nginx &> /dev/null; then
    log "Устанавливаем Nginx..."
    apt install -y nginx
    systemctl enable nginx
    systemctl start nginx
else
    log "Nginx уже установлен"
fi

# Установка Certbot для SSL
if ! command -v certbot &> /dev/null; then
    log "Устанавливаем Certbot..."
    apt install -y certbot python3-certbot-nginx
else
    log "Certbot уже установлен"
fi

# Создание директорий
log "Создаем структуру директорий..."
mkdir -p /opt/$PROJECT_NAME
mkdir -p /opt/$PROJECT_NAME/ssl
mkdir -p /opt/$PROJECT_NAME/logs
mkdir -p /opt/$PROJECT_NAME/backups
mkdir -p /opt/$PROJECT_NAME/uploads

# Создание пользователя для приложения
if ! id "$PROJECT_NAME" &>/dev/null; then
    log "Создаем пользователя $PROJECT_NAME..."
    useradd -r -s /bin/false -d /opt/$PROJECT_NAME $PROJECT_NAME
    chown -R $PROJECT_NAME:$PROJECT_NAME /opt/$PROJECT_NAME
else
    log "Пользователь $PROJECT_NAME уже существует"
fi

# Создание .env файла
log "Создаем файл конфигурации..."
cat > /opt/$PROJECT_NAME/.env << EOF
# Основные настройки
APP_NAME=Sadaka-Pass
APP_VERSION=1.0.0
DEBUG=false
ENVIRONMENT=$ENVIRONMENT

# Безопасность
SECRET_KEY=$(openssl rand -hex 32)
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256

# База данных
DATABASE_URL=postgresql://sadaka_user:$(openssl rand -hex 16)@db:5432/sadaka_pass
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20

# Redis
REDIS_URL=redis://redis:6379/0
REDIS_MAX_CONNECTIONS=20

# Elasticsearch
ELASTICSEARCH_URL=http://elasticsearch:9200
ELASTICSEARCH_INDEX_PREFIX=sadaka_pass

# Telegram
TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN_HERE
TELEGRAM_WEBAPP_URL=https://$DOMAIN
TELEGRAM_WEBHOOK_URL=https://$DOMAIN/webhook/telegram

# Платежные системы
YOOKASSA_SHOP_ID=YOUR_SHOP_ID_HERE
YOOKASSA_SECRET_KEY=YOUR_SECRET_KEY_HERE
YOOKASSA_WEBHOOK_URL=https://$DOMAIN/webhook/yookassa

CLOUDPAYMENTS_PUBLIC_ID=YOUR_PUBLIC_ID_HERE
CLOUDPAYMENTS_API_SECRET=YOUR_API_SECRET_HERE
CLOUDPAYMENTS_WEBHOOK_URL=https://$DOMAIN/webhook/cloudpayments

# Внешние API
BOT_E_REPLIKA_API_URL=https://bot.e-replika.ru
BOT_E_REPLIKA_API_TOKEN=YOUR_API_TOKEN_HERE

# CORS
ALLOWED_ORIGINS=https://t.me,https://web.telegram.org,https://$DOMAIN

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60

# Логирование
LOG_LEVEL=INFO
LOG_FORMAT=json

# Мониторинг
ENABLE_METRICS=true
ENABLE_HEALTH_CHECKS=true

# Файлы
MAX_FILE_SIZE=10485760
UPLOAD_DIR=/opt/$PROJECT_NAME/uploads

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=$EMAIL
SMTP_PASSWORD=YOUR_SMTP_PASSWORD_HERE
SMTP_USE_TLS=true

# Кэширование
CACHE_TTL_DEFAULT=300
CACHE_TTL_USER_DATA=1800
CACHE_TTL_FUND_DATA=3600
CACHE_TTL_CAMPAIGN_DATA=1800
EOF

log "Настройка завершена!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Скопируйте код приложения в /opt/$PROJECT_NAME/"
echo "2. Отредактируйте .env файл с вашими настройками"
echo "3. Получите SSL сертификат: ./get-ssl.sh $DOMAIN $EMAIL"
echo "4. Запустите приложение: docker-compose up -d"
echo "5. Включите автозапуск: systemctl enable $PROJECT_NAME"
echo ""
echo "🔧 Полезные команды:"
echo "- Мониторинг: ./monitor.sh"
echo "- Резервное копирование: ./backup.sh"
echo "- Логи: docker-compose logs -f"
echo "- Перезапуск: docker-compose restart"
echo ""
echo "🌐 После запуска приложение будет доступно по адресу: https://$DOMAIN"
echo "📊 Админ панель: https://$DOMAIN/admin"
echo "📚 API документация: https://$DOMAIN/api/docs"