# 💳 Интеграция CloudPayments

## Обзор

Проект Sadaka-Pass интегрирован с платежной системой CloudPayments для обработки пожертвований.

## Архитектура

### Backend компоненты

1. **Сервис CloudPayments** (`backend/app/services/cloudpayments_service.py`)
   - Генерация подписей для платежей
   - Создание параметров виджета
   - Проверка webhook'ов

2. **API Endpoints**
   - `POST /api/v1/donations/init` - Инициализация платежа
   - `POST /api/v1/webhooks/cloudpayments` - Обработка уведомлений

3. **Webhook** (`backend/app/api/webhooks.py`)
   - Прием уведомлений от CloudPayments
   - Проверка подписей
   - Обновление статуса платежей в БД

## Настройка

### 1. Переменные окружения

Добавьте в `.env` файл:

```env
# CloudPayments
CLOUDPAYMENTS_PUBLIC_ID=your_public_id_here
CLOUDPAYMENTS_API_SECRET=your_api_secret_here
```

### 2. Получение ключей

1. Зарегистрируйтесь в CloudPayments (https://cloudpayments.ru)
2. Создайте аккаунт и получите:
   - **Public ID** - для фронтенда (виджет)
   - **API Secret** - для бэкенда (подпись запросов)

### 3. Настройка Webhook в CloudPayments

В личном кабинете CloudPayments укажите:
```
URL: https://your-domain.com/api/v1/webhooks/cloudpayments
```

## Использование

### Backend API

#### Инициализация платежа

```python
POST /api/v1/donations/init

{
    "user_id": 1,
    "fund_id": 1,
    "amount": 1000.00,
    "currency": "RUB",
    "payment_method": "cloudpayments",
    "purpose": "Благотворительность"
}
```

**Ответ:**
```json
{
    "donation_id": 123,
    "amount": 1000.0,
    "currency": "RUB",
    "payment_method": "cloudpayments",
    "widget_params": {
        "public_id": "pk_xxxxx",
        "amount": 1000.0,
        "currency": "RUB",
        "invoice_id": "123",
        "description": "Пожертвование в фонд ...",
        "signature": "abc123..."
    },
    "widget_url": "https://widget.cloudpayments.ru/payment",
    "status": "pending"
}
```

### Frontend интеграция

#### 1. Подключение виджета

Добавьте скрипт CloudPayments в `public/index.html`:

```html
<script src="https://widget.cloudpayments.ru/bundles/checkout"></script>
```

#### 2. Запуск виджета

```typescript
import { useNavigate } from 'react-router-dom';

const processCloudPaymentsPayment = async (donationData: any) => {
  try {
    // 1. Инициализируем платеж на backend
    const response = await donationApi.init({
      user_id: currentUser.id,
      fund_id: selectedFund.id,
      amount: amount,
      currency: 'RUB',
      payment_method: 'cloudpayments',
      purpose: 'Пожертвование'
    });
    
    const { widget_params, widget_url } = response.data;
    
    // 2. Запускаем виджет
    const widget = new (window as any).cp.CloudPayments();
    
    widget.charge(
      {
        publicId: widget_params.public_id,
        description: widget_params.description,
        amount: widget_params.amount,
        currency: widget_params.currency,
        invoiceId: widget_params.invoice_id,
        accountId: widget_params.account_id,
        skin: "modern", // или "classic"
        language: "ru-RU"
      },
      function(options) {
        // Платеж успешен
        console.log('Payment successful:', options);
        showSuccess();
      },
      function(reason, options) {
        // Ошибка платежа
        console.error('Payment failed:', reason, options);
        showError(reason);
      }
    );
    
  } catch (error) {
    console.error('Error initializing payment:', error);
  }
};
```

#### 3. Обработка результатов

```typescript
// Успешный платеж
widget.onPaymentSuccess = (data: any) => {
  console.log('Payment successful:', data);
  navigate('/donation/success');
};

// Отмена платежа
widget.onPaymentCancel = () => {
  console.log('Payment cancelled');
  navigate('/donation/cancel');
};

// Ошибка платежа
widget.onPaymentError = (error: any) => {
  console.error('Payment error:', error);
  showError('Не удалось обработать платеж');
};
```

## Webhook обработка

### Формат webhook от CloudPayments

```json
{
  "TransactionId": 123456,
  "Amount": 1000.00,
  "Currency": "RUB",
  "DateTime": "2024-01-01T00:00:00",
  "CardFirstSix": "411111",
  "CardLastFour": "1111",
  "CardType": "Visa",
  "InvoiceId": "donation_123",
  "Status": "Completed",
  "Signature": "abc123..."
}
```

### Наш endpoint

```
POST /api/v1/webhooks/cloudpayments
```

**Ответ (успех):**
```json
{
  "code": 0,
  "message": "OK"
}
```

**Ответ (ошибка):**
```json
{
  "code": 1,
  "message": "Error description"
}
```

## Безопасность

### Проверка подписи

Все webhook'и от CloudPayments проходят проверку подписи:

```python
def verify_webhook_signature(
    transaction_id: str,
    amount: float,
    currency: str,
    status: str,
    signature: str
) -> bool:
    """Проверка подписи webhook"""
    data_string = f"{transaction_id}{amount}{currency}{status}"
    expected_signature = hmac.new(
        api_secret.encode('utf-8'),
        data_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(expected_signature, signature)
```

## Статусы платежей

| CloudPayments | Internal | Описание |
|---------------|-----------|----------|
| Completed | completed | Платеж успешен |
| Authorized | pending | Платеж авторизован |
| Cancelled | failed | Платеж отменен |
| Declined | failed | Платеж отклонен |
| Pending | pending | Платеж в обработке |

## Тестирование

### Тестовые карты

Для тестирования используйте карты:

**Успешная транзакция:**
- Номер: `5555 5555 5555 4444`
- CVV: любые 3 цифры
- Срок: любая будущая дата

**Отклоненная транзакция:**
- Номер: `5555 5555 5555 4477`

### Тестовый endpoint

```
GET /api/v1/webhooks/cloudpayments/test
```

Проверяет, что webhook endpoint работает.

## Развертывание

### 1. Настройка переменных окружения

```bash
export CLOUDPAYMENTS_PUBLIC_ID="pk_xxxxx"
export CLOUDPAYMENTS_API_SECRET="secret_key_here"
```

### 2. Запуск проекта

```bash
docker-compose up -d
```

### 3. Проверка webhook

```bash
curl https://your-domain.com/api/v1/webhooks/cloudpayments/test
```

## Troubleshooting

### Проблема: Webhook не принимается

**Решение:**
1. Проверьте URL в настройках CloudPayments
2. Убедитесь, что сервер доступен из интернета
3. Проверьте логи: `docker logs backend`

### Проблема: Неверная подпись

**Решение:**
1. Проверьте `CLOUDPAYMENTS_API_SECRET` в `.env`
2. Убедитесь, что используется правильный секрет для подписи

### Проблема: Платеж не проходит

**Решение:**
1. Проверьте параметры виджета
2. Убедитесь, что `invoice_id` уникален
3. Проверьте логи в панели CloudPayments

## Документация CloudPayments

- Официальная документация: https://developers.cloudpayments.ru/
- Виджет: https://widget.cloudpayments.ru/
- API: https://developers.cloudpayments.ru/api/

## Поддержка

При возникновении вопросов обращайтесь:
- Email: support@sadaka-pass.com
- Telegram: @support_sadaka

