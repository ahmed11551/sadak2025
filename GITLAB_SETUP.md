# Быстрая настройка GitLab CI/CD для Sadaka-Pass

## ⚡ Быстрый старт

### 1. Добавьте файлы в Git

```bash
git add .gitlab-ci.yml
git add .gitignore
git add env.gitlab.example
git add docker-compose.prod.yml
git commit -m "feat: add GitLab CI/CD configuration"
git push origin main
```

### 2. Настройте CI/CD переменные

1. Откройте GitLab: Settings → CI/CD → Variables
2. Добавьте переменные из `env.gitlab.example`
3. Для безопасности используйте переменные типа "Masked" и "Protected"

**Обязательные переменные:**
- `CI_REGISTRY_USER` - пользователь Docker Registry
- `CI_REGISTRY_PASSWORD` - пароль Docker Registry  
- `SSH_PRIVATE_KEY` - приватный SSH ключ для деплоя
- `STAGING_SERVER` - домен/IP staging сервера
- `STAGING_USER` - SSH пользователь для staging
- `PRODUCTION_SERVER` - домен/IP production сервера
- `PRODUCTION_USER` - SSH пользователь для production
- `POSTGRES_PASSWORD` - пароль PostgreSQL
- `SECRET_KEY` - секретный ключ приложения
- `TELEGRAM_BOT_TOKEN` - токен Telegram бота
- `YOOKASSA_SHOP_ID` - ID магазина YooKassa
- `YOOKASSA_SECRET_KEY` - секретный ключ YooKassa

### 3. Настройте Docker Runner

Создайте файл `/etc/gitlab-runner/config.toml`:

```toml
concurrent = 4

[[runners]]
  name = "Docker Runner"
  url = "https://your-gitlab.com/"
  token = "your-token"
  executor = "docker"
  [runners.docker]
    image = "docker:24.0.5"
    privileged = true
    volumes = ["/cache"]
    services = ["docker:24.0.5-dind"]
```

### 4. Подготовьте staging сервер

```bash
# На сервере
cd /opt
sudo mkdir sadaka
sudo chown $USER:$USER sadaka
cd sadaka

# Склонируйте репозиторий
git clone https://gitlab.com/your-username/sadaka-pass.git .

# Создайте .env файл
cp env.example .env
nano .env  # Отредактируйте значения

# Настройте SSH ключи для деплоя
ssh-keygen -t rsa -b 4096 -C "gitlab-ci@staging"
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys

# Добавьте приватный ключ в GitLab CI/CD переменные
cat ~/.ssh/id_rsa
# Скопируйте и вставьте как SSH_PRIVATE_KEY
```

### 5. Подготовьте production сервер

Аналогично staging, но с production конфигурацией.

### 6. Развертывание

#### Staging (автоматически при push в develop):
```bash
git checkout develop
git merge feature/your-feature
git push origin develop
# Pipeline запустится автоматически
```

#### Production (ручной деплой):
1. Войдите в main ветку
2. Слейте изменения из develop
3. Запушьте в main
4. Pipeline запустится, дождитесь всех stages
5. Нажмите "Play" на stage "Deploy to Production"

## 📊 Проверка работы

После деплоя проверьте:

- **Backend API**: https://your-domain.com/api/docs
- **Frontend**: https://your-domain.com
- **Admin Panel**: https://your-domain.com/admin
- **Health Check**: https://your-domain.com/api/health

## 🔧 Полезные команды

```bash
# Просмотр pipeline
# GitLab → CI/CD → Pipelines

# Просмотр логов
# GitLab → CI/CD → Pipelines → [Pipeline] → [Job] → View log

# Локальная проверка
gitlab-runner exec docker lint:backend
gitlab-runner exec docker test:backend
```

## 🐛 Troubleshooting

### Pipeline не запускается
- Проверьте наличие `.gitlab-ci.yml`
- Убедитесь что есть активный runner
- Проверьте Settings → CI/CD → Runners

### Docker build падает
- Проверьте доступ к Docker Registry
- Убедитесь что Docker-in-Docker настроен
- Проверьте Dockerfile

### Деплой не работает
- Проверьте SSH ключ
- Убедитесь что пользователь имеет права на директорию
- Проверьте доступность сервера

## 📚 Дополнительная документация

- [Полная документация GitLab CI](docs/GITLAB_CI_SETUP.md)
- [Техническая документация](docs/TECHNICAL_DOCUMENTATION.md)
- [API документация](docs/API.md)

## ✅ Чеклист

- [ ] GitLab репозиторий создан
- [ ] `.gitlab-ci.yml` залит в репозиторий
- [ ] CI/CD переменные настроены
- [ ] Docker Runner установлен и зарегистрирован
- [ ] Staging сервер подготовлен
- [ ] Production сервер подготовлен
- [ ] SSH ключи настроены
- [ ] Pipeline успешно запускается
- [ ] Тесты проходят
- [ ] Деплой работает

---

**Готово! 🚀**

