import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import tempfile
import os

from app.main import app
from app.core.database import get_db, Base
from app.models.models import User, Fund, Campaign, SubscriptionPlan

# Создаем тестовую базу данных в памяти
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="function")
def db_session():
    """Создает тестовую сессию БД для каждого теста"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_user(db_session):
    """Создает тестового пользователя"""
    user = User(
        telegram_id=123456789,
        username="testuser",
        first_name="Test",
        last_name="User",
        language_code="ru"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def test_fund(db_session):
    """Создает тестовый фонд"""
    fund = Fund(
        name="Test Fund",
        description="Test fund description",
        country_code="RU",
        purposes=["mosque", "orphans"],
        verified=True,
        active=True
    )
    db_session.add(fund)
    db_session.commit()
    db_session.refresh(fund)
    return fund

@pytest.fixture
def test_campaign(db_session, test_user, test_fund):
    """Создает тестовую кампанию"""
    campaign = Campaign(
        owner_id=test_user.id,
        fund_id=test_fund.id,
        title="Test Campaign",
        description="Test campaign description",
        category="mosque",
        goal_amount=100000,
        country_code="RU",
        status="active"
    )
    db_session.add(campaign)
    db_session.commit()
    db_session.refresh(campaign)
    return campaign

@pytest.fixture
def test_subscription_plan(db_session):
    """Создает тестовый тарифный план"""
    plan = SubscriptionPlan(
        name="basic",
        display_name="Базовый",
        description="Базовый план",
        price_monthly=290,
        price_3months=870,
        charity_percentage=0,
        features=["basic_access", "notifications"]
    )
    db_session.add(plan)
    db_session.commit()
    db_session.refresh(plan)
    return plan


class TestHealthCheck:
    """Тесты для health check эндпоинта"""
    
    def test_health_check(self):
        """Тест проверки здоровья системы"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["database"] == "connected"


class TestUsersAPI:
    """Тесты для API пользователей"""
    
    def test_create_user(self, db_session):
        """Тест создания пользователя"""
        user_data = {
            "telegram_id": 987654321,
            "username": "newuser",
            "first_name": "New",
            "last_name": "User",
            "language_code": "ru"
        }
        
        response = client.post("/api/v1/users/", json=user_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["telegram_id"] == user_data["telegram_id"]
        assert data["username"] == user_data["username"]
        assert data["first_name"] == user_data["first_name"]
        assert data["is_active"] == True
    
    def test_get_user_by_telegram_id(self, db_session, test_user):
        """Тест получения пользователя по Telegram ID"""
        response = client.get(f"/api/v1/users/telegram/{test_user.telegram_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == test_user.id
        assert data["telegram_id"] == test_user.telegram_id
    
    def test_get_user_not_found(self, db_session):
        """Тест получения несуществующего пользователя"""
        response = client.get("/api/v1/users/telegram/999999999")
        assert response.status_code == 404


class TestFundsAPI:
    """Тесты для API фондов"""
    
    def test_get_funds(self, db_session, test_fund):
        """Тест получения списка фондов"""
        response = client.get("/api/v1/funds/")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == test_fund.name
        assert data[0]["verified"] == True
    
    def test_get_funds_with_filters(self, db_session, test_fund):
        """Тест получения фондов с фильтрами"""
        response = client.get("/api/v1/funds/?country_code=RU&verified_only=true")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 1
        assert data[0]["country_code"] == "RU"
    
    def test_get_fund_by_id(self, db_session, test_fund):
        """Тест получения фонда по ID"""
        response = client.get(f"/api/v1/funds/{test_fund.id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == test_fund.id
        assert data["name"] == test_fund.name
    
    def test_search_funds(self, db_session, test_fund):
        """Тест поиска фондов"""
        response = client.get("/api/v1/funds/search/?q=Test")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 1
        assert "Test" in data[0]["name"]


class TestCampaignsAPI:
    """Тесты для API кампаний"""
    
    def test_get_campaigns(self, db_session, test_campaign):
        """Тест получения списка кампаний"""
        response = client.get("/api/v1/campaigns/")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == test_campaign.title
        assert data[0]["status"] == "active"
    
    def test_get_campaign_by_id(self, db_session, test_campaign):
        """Тест получения кампании по ID"""
        response = client.get(f"/api/v1/campaigns/{test_campaign.id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == test_campaign.id
        assert data["title"] == test_campaign.title
    
    def test_create_campaign(self, db_session, test_user, test_fund):
        """Тест создания кампании"""
        campaign_data = {
            "fund_id": test_fund.id,
            "title": "New Campaign",
            "description": "New campaign description",
            "category": "orphans",
            "goal_amount": 50000,
            "country_code": "RU"
        }
        
        response = client.post(f"/api/v1/campaigns/?user_id={test_user.id}", json=campaign_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["title"] == campaign_data["title"]
        assert data["owner_id"] == test_user.id
        assert data["status"] == "pending"
    
    def test_donate_to_campaign(self, db_session, test_campaign, test_user):
        """Тест пожертвования в кампанию"""
        donation_data = {
            "user_id": test_user.id,
            "amount": 1000,
            "currency": "RUB",
            "payment_method": "yookassa"
        }
        
        response = client.post(f"/api/v1/campaigns/{test_campaign.id}/donate", json=donation_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["amount"] == 1000
        assert data["campaign_progress"] > 0


class TestZakatAPI:
    """Тесты для API закята"""
    
    def test_calculate_zakat(self, db_session, test_user):
        """Тест расчета закята"""
        zakat_data = {
            "cash_at_home": 100000,
            "bank_accounts": 500000,
            "debts": 50000,
            "expenses": 20000
        }
        
        response = client.post(f"/api/v1/zakat/calc?user_id={test_user.id}", json=zakat_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["total_assets"] == 600000
        assert data["total_liabilities"] == 70000
        assert data["zakatable_amount"] == 530000
        assert data["zakat_amount"] > 0  # Должен быть больше нисаба
    
    def test_get_current_nisab(self):
        """Тест получения текущего нисаба"""
        response = client.get("/api/v1/zakat/nisab")
        assert response.status_code == 200
        
        data = response.json()
        assert "nisab_amount" in data
        assert "currency" in data
        assert "zakat_rate" in data


class TestPartnersAPI:
    """Тесты для API партнеров"""
    
    def test_create_partner_application(self, db_session):
        """Тест создания заявки на партнерство"""
        application_data = {
            "organization_name": "Test Organization",
            "contact_person": "John Doe",
            "email": "test@example.com",
            "phone": "+1234567890",
            "website": "https://test.org",
            "description": "Test organization description",
            "purposes": ["mosque", "orphans"]
        }
        
        response = client.post("/api/v1/partners/applications", json=application_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["organization_name"] == application_data["organization_name"]
        assert data["status"] == "pending"
    
    def test_get_partner_applications(self, db_session):
        """Тест получения заявок на партнерство"""
        response = client.get("/api/v1/partners/applications")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)


class TestErrorHandling:
    """Тесты для обработки ошибок"""
    
    def test_invalid_endpoint(self):
        """Тест несуществующего эндпоинта"""
        response = client.get("/api/v1/invalid")
        assert response.status_code == 404
    
    def test_invalid_data_format(self):
        """Тест неверного формата данных"""
        response = client.post("/api/v1/users/", json={"invalid": "data"})
        assert response.status_code == 422
    
    def test_missing_required_fields(self):
        """Тест отсутствующих обязательных полей"""
        response = client.post("/api/v1/users/", json={})
        assert response.status_code == 422


# Интеграционные тесты
class TestIntegration:
    """Интеграционные тесты"""
    
    def test_full_donation_flow(self, db_session, test_user, test_fund):
        """Тест полного потока пожертвования"""
        # 1. Создаем пожертвование
        donation_data = {
            "fund_id": test_fund.id,
            "amount": 1000,
            "currency": "RUB",
            "payment_method": "yookassa"
        }
        
        response = client.post("/api/v1/donations/init", json=donation_data)
        assert response.status_code == 200
        
        donation_response = response.json()
        donation_id = donation_response["donation_id"]
        
        # 2. Подтверждаем платеж
        payment_data = {
            "payment_id": "test_payment_123",
            "transaction_id": "test_transaction_456"
        }
        
        response = client.post(f"/api/v1/donations/{donation_id}/confirm", json=payment_data)
        assert response.status_code == 200
        
        # 3. Проверяем историю пользователя
        response = client.get(f"/api/v1/users/{test_user.id}/donations")
        assert response.status_code == 200
        
        donations = response.json()
        assert len(donations) == 1
        assert donations[0]["amount"] == 1000
        assert donations[0]["status"] == "completed"
    
    def test_campaign_lifecycle(self, db_session, test_user, test_fund):
        """Тест жизненного цикла кампании"""
        # 1. Создаем кампанию
        campaign_data = {
            "fund_id": test_fund.id,
            "title": "Lifecycle Test Campaign",
            "description": "Test campaign for lifecycle",
            "category": "mosque",
            "goal_amount": 10000,
            "country_code": "RU"
        }
        
        response = client.post(f"/api/v1/campaigns/?user_id={test_user.id}", json=campaign_data)
        assert response.status_code == 200
        
        campaign = response.json()
        campaign_id = campaign["id"]
        
        # 2. Делаем пожертвование в кампанию
        donation_data = {
            "user_id": test_user.id,
            "amount": 5000,
            "currency": "RUB",
            "payment_method": "yookassa"
        }
        
        response = client.post(f"/api/v1/campaigns/{campaign_id}/donate", json=donation_data)
        assert response.status_code == 200
        
        # 3. Проверяем прогресс кампании
        response = client.get(f"/api/v1/campaigns/{campaign_id}")
        assert response.status_code == 200
        
        campaign_data = response.json()
        assert campaign_data["collected_amount"] == 5000
        assert campaign_data["participants_count"] == 1
        
        # 4. Завершаем кампанию
        response = client.post(f"/api/v1/campaigns/{campaign_id}/complete")
        assert response.status_code == 200
        
        # 5. Проверяем статус
        response = client.get(f"/api/v1/campaigns/{campaign_id}")
        assert response.status_code == 200
        
        campaign_data = response.json()
        assert campaign_data["status"] == "completed"
