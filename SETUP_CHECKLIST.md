# ✅ Чеклист настройки GitLab CI/CD для Sadaka-Pass

## 📋 Шаг 1: Проверка файлов проекта

Убедитесь что у вас есть все необходимые файлы:

- [ ] `.gitlab-ci.yml` - конфигурация GitLab CI/CD
- [ ] `.gitignore` - файлы для исключения из git
- [ ] `docker-compose.yml` - development окружение
- [ ] `docker-compose.prod.yml` - production окружение
- [ ] `env.example` - пример переменных окружения
- [ ] `env.gitlab.example` - переменные для GitLab CI/CD
- [ ] `nginx/nginx.conf` - конфигурация Nginx
- [ ] `admin-panel/Dockerfile` - Dockerfile для админ-панели

Все компоненты имеют Dockerfile:
- [ ] `backend/Dockerfile`
- [ ] `frontend/Dockerfile`
- [ ] `admin-panel/Dockerfile`
- [ ] `telegram-bot/Dockerfile`

## 📦 Шаг 2: Настройка Git репозитория

### 2.1 Инициализация Git (если еще не сделано)

```bash
cd C:\Users\Dev-Ops\Desktop\sadaka
git init
```

### 2.2 Добавление всех файлов

```bash
# Добавим конфигурацию CI/CD
git add .gitlab-ci.yml .gitignore
git add env.gitlab.example docker-compose.prod.yml
git add nginx/ admin-panel/Dockerfile

# Добавим код проекта
git add backend/ frontend/ telegram-bot/ admin-panel/
git add docs/ scripts/

# Фиксируем изменения
git commit -m "feat: initial project setup with GitLab CI/CD"
```

### 2.3 Добавление удаленного репозитория

```bash
# Замените YOUR_GITLAB_URL на ваш GitLab URL
git remote add origin https://gitlab.com/your-username/sadaka-pass.git
git branch -M main
git push -u origin main
```

## 🔧 Шаг 3: Настройка GitLab CI/CD

### 3.1 Создание проекта в GitLab

1. Войдите в GitLab
2. Создайте новый проект: **New Project** → **Import repository**
3. Скопируйте URL вашего репозитория или загрузите файлы

### 3.2 Настройка Runner

**Важно:** Нужен Docker Runner с поддержкой Docker-in-Docker

#### Опция A: Использование GitLab.com Runners (Shared Runners)
- Просто включите Shared Runners в настройках проекта
- Settings → CI/CD → Runners → Enable shared runners

#### Опция B: Собственный Runner
Создайте файл `config.toml`:

```toml
concurrent = 4

[[runners]]
  name = "Docker Runner"
  url = "https://gitlab.com/"
  token = "YOUR_TOKEN"
  executor = "docker"
  [runners.docker]
    image = "docker:24.0.5"
    privileged = true
    volumes = ["/cache"]
    services = ["docker:24.0.5-dind"]
```

### 3.3 Настройка переменных окружения

Перейдите: **Settings** → **CI/CD** → **Variables** → **Add variable**

Добавьте следующие переменные:

#### Обязательные переменные:

| Переменная | Значение | Защищено | Маскировано |
|------------|----------|----------|-------------|
| `CI_REGISTRY_USER` | ваш_пользователь | ✅ | ❌ |
| `CI_REGISTRY_PASSWORD` | ваш_пароль | ✅ | ✅ |
| `SSH_PRIVATE_KEY` | приватный_ключ | ✅ | ✅ |
| `STAGING_SERVER` | staging.domain.com | ❌ | ❌ |
| `STAGING_USER` | deploy | ❌ | ❌ |
| `PRODUCTION_SERVER` | domain.com | ❌ | ❌ |
| `PRODUCTION_USER` | deploy | ❌ | ❌ |
| `POSTGRES_PASSWORD` | сложный_пароль | ✅ | ✅ |
| `SECRET_KEY` | секретный_ключ | ✅ | ✅ |
| `TELEGRAM_BOT_TOKEN` | токен_бота | ✅ | ✅ |
| `YOOKASSA_SHOP_ID` | id_магазина | ✅ | ❌ |
| `YOOKASSA_SECRET_KEY` | секретный_ключ | ✅ | ✅ |

#### Как получить SSH ключ:

```bash
# На вашем компьютере или сервере
ssh-keygen -t rsa -b 4096 -C "gitlab-ci@your-domain.com"

# Скопируйте приватный ключ для SSH_PRIVATE_KEY
cat ~/.ssh/id_rsa

# Добавьте публичный ключ на сервера
cat ~/.ssh/id_rsa.pub | ssh user@server "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

## 🖥️ Шаг 4: Подготовка серверов

### 4.1 Подготовка Staging сервера

```bash
# SSH подключитесь к staging серверу
ssh deploy@staging.sadaka-pass.com

# Установите Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Установите Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Создайте директорию для проекта
sudo mkdir -p /opt/sadaka
sudo chown $USER:$USER /opt/sadaka
cd /opt/sadaka

# Склонируйте репозиторий
git clone https://gitlab.com/your-username/sadaka-pass.git .

# Создайте .env файл
cp env.example .env
nano .env  # Отредактируйте с реальными значениями

# Создайте директорию для SSL
mkdir -p nginx/ssl

# Добавьте SSL сертификаты в nginx/ssl/
# Или используйте Let's Encrypt:
sudo apt-get install certbot
sudo certbot certonly --standalone -d staging.sadaka-pass.com
sudo cp /etc/letsencrypt/live/staging.sadaka-pass.com/fullchain.pem nginx/ssl/
sudo cp /etc/letsencrypt/live/staging.sadaka-pass.com/privkey.pem nginx/ssl/
sudo chown $USER:$USER nginx/ssl/*
```

### 4.2 Подготовка Production сервера

Аналогично staging, но:
- Используйте production домен
- Используйте более строгие настройки безопасности
- Настройте автоматическое обновление SSL сертификатов

```bash
# Настройте автообновление SSL
sudo crontab -e
# Добавьте:
0 3 * * 0 certbot renew --quiet && docker-compose -f /opt/sadaka/docker-compose.prod.yml restart nginx
```

## 🚀 Шаг 5: Первый запуск Pipeline

### 5.1 Запуск на Staging

```bash
# Создайте ветку develop
git checkout -b develop

# Сделайте любое небольшое изменение (например, обновите README)
echo "# Test" >> README.md
git add README.md
git commit -m "test: initial CI/CD test"
git push origin develop

# Pipeline запустится автоматически!
```

### 5.2 Проверка Pipeline

1. Откройте GitLab → CI/CD → Pipelines
2. Дождитесь завершения всех стадий
3. Проверьте логи на наличие ошибок

### 5.3 Проверка деплоя

После успешного деплоя проверьте:

```bash
# Проверьте, что контейнеры запущены
ssh deploy@staging.sadaka-pass.com
cd /opt/sadaka
docker-compose -f docker-compose.prod.yml ps

# Проверьте логи
docker-compose -f docker-compose.prod.yml logs backend
docker-compose -f docker-compose.prod.yml logs frontend
```

## 🎯 Шаг 6: Production деплой

### 6.1 Подготовка к production деплою

```bash
# Слейте develop в main
git checkout main
git merge develop
git push origin main

# Откройте Pipeline и запустите "Deploy to Production" вручную
# (Стадия require manual intervention)
```

### 6.2 Проверка production

После деплоя проверьте все сервисы:

- ✅ Backend API: https://your-domain.com/api/docs
- ✅ Frontend: https://your-domain.com  
- ✅ Admin Panel: https://your-domain.com/admin
- ✅ Health Check: https://your-domain.com/api/health

## 🔍 Шаг 7: Мониторинг и логирование

### Настройте мониторинг:

```bash
# На серверах добавьте логирование
cd /opt/sadaka
docker-compose -f docker-compose.prod.yml exec backend tail -f /app/logs/app.log
```

## ✅ Финальная проверка

После настройки убедитесь что:

- [ ] Pipeline успешно запускается при push в develop
- [ ] Все тесты проходят
- [ ] Docker образы собираются
- [ ] Деплой на staging работает
- [ ] Все сервисы доступны
- [ ] SSL сертификаты установлены
- [ ] Логирование работает
- [ ] Health checks проходят

## 📚 Дополнительные ресурсы

- [GITLAB_SETUP.md](GITLAB_SETUP.md) - быстрая настройка
- [docs/GITLAB_CI_SETUP.md](docs/GITLAB_CI_SETUP.md) - подробная документация
- [docs/TECHNICAL_DOCUMENTATION.md](docs/TECHNICAL_DOCUMENTATION.md) - техническая документация

## 🆘 Помощь

Если возникли проблемы:

1. Проверьте логи Pipeline в GitLab
2. Проверьте логи Docker контейнеров на сервере
3. Убедитесь что все переменные окружения настроены
4. Проверьте SSH доступ к серверам
5. Проверьте что Runner доступен

---

**Готово! 🎉** Ваш проект настроен для автоматического развертывания через GitLab CI/CD!

