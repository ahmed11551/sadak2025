# GitLab CI/CD Setup для Sadaka-Pass

## 📋 Обзор

Этот документ описывает настройку и использование GitLab CI/CD pipeline для автоматизации сборки, тестирования и развертывания проекта Sadaka-Pass.

## 🔧 Требования

- GitLab репозиторий
- Docker Runner с Docker-in-Docker
- Серверы для staging и production окружений
- SSH доступ к серверам развертывания

## 🚀 Настройка

### 1. CI/CD Variables

Настройте следующие переменные в GitLab: Settings → CI/CD → Variables

#### Обязательные переменные:

```
CI_REGISTRY_USER        # Пользователь Docker Registry
CI_REGISTRY_PASSWORD    # Пароль Docker Registry
SSH_PRIVATE_KEY         # Приватный SSH ключ для деплоя
STAGING_SERVER          # IP/домен staging сервера
STAGING_USER            # SSH пользователь staging
PRODUCTION_SERVER       # IP/домен production сервера
PRODUCTION_USER         # SSH пользователь production
```

### 2. Docker Runner

Убедитесь, что у вас настроен Docker Runner с Docker-in-Docker:

```toml
# config.toml
[[runners]]
  name = "Docker Runner"
  url = "https://gitlab.com/"
  token = "your-token"
  executor = "docker"
  [runners.docker]
    image = "docker:24.0.5"
    privileged = true
    volumes = ["/cache"]
    services = ["docker:24.0.5-dind"]
```

### 3. Настройка серверов

#### На staging/production серверах:

```bash
# Установите Docker и Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Создайте директорию для проекта
sudo mkdir -p /opt/sadaka
sudo chown $USER:$USER /opt/sadaka

# Склонируйте репозиторий
cd /opt/sadaka
git clone https://gitlab.com/your-username/sadaka-pass.git .

# Создайте .env файл
cp env.example .env
# Отредактируйте .env с реальными значениями
```

### 4. SSH ключи для деплоя

На серверах создайте SSH ключ и добавьте публичный ключ в authorized_keys:

```bash
# На сервере
ssh-keygen -t rsa -b 4096 -C "gitlab-ci@your-domain.com"
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
chmod 700 ~/.ssh
```

Добавьте приватный ключ в GitLab CI/CD переменные как `SSH_PRIVATE_KEY`.

## 📊 Pipeline Stages

### 1. Lint Stage
- Проверка кода с помощью линтеров
- Backend: Black, Flake8, isort, mypy
- Frontend: ESLint, Prettier
- Запускается при изменениях в соответствующих директориях

### 2. Test Stage
- Unit и Integration тесты
- Проверка покрытия кода
- Запускается при изменениях в соответствующих директориях

### 3. Build Stage
- Сборка Docker образов
- Публикация в Container Registry
- Тегирование: `latest` и `branch-commit`

### 4. Deploy Stage
- Автоматический деплой на staging (develop ветка)
- Ручной деплой на production (main ветка)
- Применение миграций БД
- Health check после деплоя

## 🔄 Workflow

### Development Flow

```bash
# Создайте feature ветку
git checkout -b feature/new-feature

# Внесите изменения и закоммитьте
git add .
git commit -m "feat: add new feature"

# Отправьте в GitLab
git push origin feature/new-feature

# Создайте Merge Request
# После ревью и апрува, влейте в develop
```

### Staging Deploy

При пуше в `develop` ветку автоматически:
- Запускается pipeline
- Выполняются линтинг и тесты
- Собираются Docker образы
- Деплоится на staging
- Проверяется health check

### Production Deploy

При влитии в `main` ветку:
- Аналогично staging
- Но деплой требует ручного подтверждения (when: manual)
- Health check выполняется после деплоя

## 🐛 Troubleshooting

### Pipeline не запускается

1. Проверьте настройки CI/CD в Settings
2. Убедитесь что есть Docker Runner
3. Проверьте наличие .gitlab-ci.yml файла

### Тесты падают

1. Проверьте логи в pipeline
2. Убедитесь что все зависимости установлены
3. Проверьте переменные окружения

### Деплой не работает

1. Проверьте SSH ключ в переменных
2. Убедитесь что пользователь имеет права на /opt/sadaka
3. Проверьте доступ к Docker Registry
4. Проверьте сетевую доступность сервера

### Docker build падает

1. Проверьте Dockerfile
2. Убедитесь что Docker-in-Docker настроен правильно
3. Проверьте доступ к Registry

## 📈 Мониторинг

После успешного деплоя проверьте:

- Backend API: https://your-domain.com/api/docs
- Frontend: https://your-domain.com
- Admin Panel: https://your-domain.com/admin
- Health Check: https://your-domain.com/api/health

## 🔒 Безопасность

1. **Никогда не коммитьте** `.env` файлы
2. Храните секреты в GitLab CI/CD Variables
3. Используйте Protected branches для main/master
4. Настройте branch protection rules
5. Используйте HTTPS для всех соединений

## 📝 Полезные команды

```bash
# Локальный запуск Docker Compose
docker-compose up -d

# Просмотр логов
docker-compose logs -f backend

# Применение миграций
docker-compose exec backend alembic upgrade head

# Вход в контейнер
docker-compose exec backend bash

# Пересборка образа
docker-compose build --no-cache backend
docker-compose up -d backend

# Очистка неиспользуемых образов
docker system prune -a
```

## 🎯 Best Practices

1. **Тестируйте локально** перед пушем
2. **Делайте маленькие коммиты** для быстрого фидбэка
3. **Используйте conventional commits** для автоматического changelog
4. **Регулярно обновляйте** зависимости
5. **Мониторьте** метрики производительности
6. **Делайте бэкапы** БД перед деплоем
7. **Проверяйте логи** после каждого деплоя

## 📚 Дополнительная документация

- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)

---

**Версия:** 1.0  
**Последнее обновление:** Январь 2024

