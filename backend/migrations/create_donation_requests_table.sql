-- Миграция: создание таблицы donation_requests
-- Дата: 2025-01-15
-- Описание: Таблица для хранения заявок на пожертвование (без реальной оплаты)

CREATE TABLE IF NOT EXISTS donation_requests (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  phone VARCHAR(50) NOT NULL,
  email VARCHAR(255),
  amount NUMERIC(10,2) NOT NULL,
  currency VARCHAR(3) DEFAULT 'RUB',
  fund_id INTEGER,
  purpose TEXT,
  message TEXT,
  status VARCHAR(50) DEFAULT 'pending',
  processed_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP
);

-- Добавляем внешний ключ к таблице funds
ALTER TABLE donation_requests 
ADD CONSTRAINT fk_donation_requests_fund 
FOREIGN KEY (fund_id) REFERENCES funds(id) ON DELETE SET NULL;

-- Индексы для быстрого поиска
CREATE INDEX IF NOT EXISTS idx_donation_requests_status ON donation_requests(status);
CREATE INDEX IF NOT EXISTS idx_donation_requests_created_at ON donation_requests(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_donation_requests_fund_id ON donation_requests(fund_id);

-- Комментарии к таблице и колонкам
COMMENT ON TABLE donation_requests IS 'Заявки на пожертвование (без реальной оплаты)';
COMMENT ON COLUMN donation_requests.id IS 'Уникальный идентификатор заявки';
COMMENT ON COLUMN donation_requests.name IS 'Имя заявителя';
COMMENT ON COLUMN donation_requests.phone IS 'Телефон заявителя';
COMMENT ON COLUMN donation_requests.email IS 'Email заявителя (опционально)';
COMMENT ON COLUMN donation_requests.amount IS 'Сумма пожертвования';
COMMENT ON COLUMN donation_requests.currency IS 'Валюта (RUB, USD, EUR и т.д.)';
COMMENT ON COLUMN donation_requests.fund_id IS 'ID фонда (если указан)';
COMMENT ON COLUMN donation_requests.purpose IS 'Назначение пожертвования';
COMMENT ON COLUMN donation_requests.message IS 'Дополнительное сообщение';
COMMENT ON COLUMN donation_requests.status IS 'Статус: pending, processed, rejected';
COMMENT ON COLUMN donation_requests.processed_at IS 'Дата обработки заявки';
COMMENT ON COLUMN donation_requests.created_at IS 'Дата создания заявки';
COMMENT ON COLUMN donation_requests.updated_at IS 'Дата последнего обновления';

