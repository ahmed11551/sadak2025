from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Numeric, JSON, Date, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
import enum


class User(Base):
    """Пользователь системы"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True, nullable=False)
    username = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    language_code = Column(String(10), default="ru")
    locale = Column(String(10), default="ru")
    timezone = Column(String(50), default="UTC")
    madhab = Column(String(50), nullable=True)  # Мазхаб пользователя
    is_premium = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    donations = relationship("Donation", back_populates="user")
    subscriptions = relationship("Subscription", back_populates="user")
    zakat_calculations = relationship("ZakatCalculation", back_populates="user")
    campaigns = relationship("Campaign", back_populates="owner")
    campaign_donations = relationship("CampaignDonation", back_populates="user")


class Fund(Base):
    """Фонд для пожертвований"""
    __tablename__ = "funds"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    short_desc = Column(Text, nullable=True)
    country_code = Column(String(3), nullable=False)  # ISO country code
    purposes = Column(JSON, nullable=True)  # Список целей фонда
    logo_url = Column(String(500), nullable=True)
    website = Column(String(500), nullable=True)
    social_links = Column(JSON, nullable=True)
    partner_enabled = Column(Boolean, default=False)
    verified = Column(Boolean, default=False)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    donations = relationship("Donation", back_populates="fund")
    subscriptions = relationship("Subscription", back_populates="fund")
    campaigns = relationship("Campaign", back_populates="fund")
    reports = relationship("Report", back_populates="fund")


class Donation(Base):
    """Разовое пожертвование"""
    __tablename__ = "donations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    fund_id = Column(Integer, ForeignKey("funds.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), default="RUB")
    purpose = Column(String(255), nullable=True)
    payment_method = Column(String(50), nullable=False)  # yookassa, cloudpayments
    payment_id = Column(String(255), nullable=True)  # ID платежа в системе
    status = Column(String(50), default="pending")  # pending, completed, failed, refunded
    transaction_id = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="donations")
    fund = relationship("Fund", back_populates="donations")


class Subscription(Base):
    """Подписка на регулярные пожертвования"""
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plan_id = Column(Integer, ForeignKey("subscription_plans.id"), nullable=False)
    fund_id = Column(Integer, ForeignKey("funds.id"), nullable=True)  # Опционально для садака-джария
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), default="RUB")
    period = Column(String(20), nullable=False)  # 1M, 3M, 6M, 12M
    purpose = Column(String(255), nullable=True)
    payment_method = Column(String(50), nullable=False)
    subscription_id = Column(String(255), nullable=True)  # ID подписки в системе
    status = Column(String(50), default="active")  # active, paused, cancelled
    next_payment_date = Column(DateTime(timezone=True), nullable=True)
    charity_amount = Column(Numeric(10, 2), default=0)  # Сумма в благотворительность
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="subscriptions")
    plan = relationship("SubscriptionPlan")
    fund = relationship("Fund", back_populates="subscriptions")
    derived_alms = relationship("DerivedAlms", back_populates="subscription")


class DerivedAlms(Base):
    """Производные пожертвования (садака-джария)"""
    __tablename__ = "derived_alms"
    
    id = Column(Integer, primary_key=True, index=True)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), default="RUB")
    purpose = Column(String(255), nullable=True)
    status = Column(String(50), default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    subscription = relationship("Subscription", back_populates="derived_alms")


class ZakatCalculation(Base):
    """Расчет закята"""
    __tablename__ = "zakat_calculations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Активы
    cash_at_home = Column(Numeric(10, 2), default=0)
    bank_accounts = Column(Numeric(10, 2), default=0)
    shares_value = Column(Numeric(10, 2), default=0)
    goods_profit = Column(Numeric(10, 2), default=0)
    gold_silver_value = Column(Numeric(10, 2), default=0)
    property_investments = Column(Numeric(10, 2), default=0)
    other_income = Column(Numeric(10, 2), default=0)
    
    # Обязательства
    debts = Column(Numeric(10, 2), default=0)
    expenses = Column(Numeric(10, 2), default=0)
    
    # Расчеты
    total_assets = Column(Numeric(10, 2), default=0)
    total_liabilities = Column(Numeric(10, 2), default=0)
    zakatable_amount = Column(Numeric(10, 2), default=0)
    nisab_amount = Column(Numeric(10, 2), default=952389)  # Текущий нисаб
    zakat_amount = Column(Numeric(10, 2), default=0)
    
    # Статус
    is_paid = Column(Boolean, default=False)
    payment_id = Column(String(255), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="zakat_calculations")


class PartnerApplication(Base):
    """Заявка на партнерство"""
    __tablename__ = "partner_applications"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_name = Column(String(255), nullable=False)
    contact_person = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=True)
    website = Column(String(500), nullable=True)
    description = Column(Text, nullable=False)
    purposes = Column(JSON, nullable=True)  # Цели организации
    documents = Column(JSON, nullable=True)  # Прикрепленные документы
    status = Column(String(50), default="pending")  # pending, approved, rejected
    reviewed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    review_notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Campaign(Base):
    """Целевая кампания"""
    __tablename__ = "campaigns"
    
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    fund_id = Column(Integer, ForeignKey("funds.id"), nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(100), nullable=False)  # mosque, orphans, medical, education, etc.
    goal_amount = Column(Numeric(10, 2), nullable=False)
    collected_amount = Column(Numeric(10, 2), default=0)
    country_code = Column(String(3), nullable=False)
    status = Column(String(50), default="pending")  # pending, active, completed, cancelled
    end_date = Column(Date, nullable=True)
    banner_url = Column(String(500), nullable=True)
    participants_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    owner = relationship("User", back_populates="campaigns")
    fund = relationship("Fund", back_populates="campaigns")
    donations = relationship("CampaignDonation", back_populates="campaign")


class CampaignDonation(Base):
    """Пожертвование в кампанию"""
    __tablename__ = "campaign_donations"
    
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), default="RUB")
    payment_method = Column(String(50), nullable=False)
    payment_id = Column(String(255), nullable=True)
    status = Column(String(50), default="pending")
    transaction_id = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    campaign = relationship("Campaign", back_populates="donations")
    user = relationship("User", back_populates="campaign_donations")


class SubscriptionPlan(Base):
    """Тарифный план подписки"""
    __tablename__ = "subscription_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)  # basic, pro, premium
    display_name = Column(String(100), nullable=False)  # Базовый, Pro, Premium
    description = Column(Text, nullable=True)
    price_monthly = Column(Numeric(10, 2), nullable=False)
    price_3months = Column(Numeric(10, 2), nullable=True)
    price_6months = Column(Numeric(10, 2), nullable=True)
    price_12months = Column(Numeric(10, 2), nullable=True)
    charity_percentage = Column(Numeric(5, 2), default=0)  # Процент в благотворительность
    features = Column(JSON, nullable=True)  # Список возможностей
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Report(Base):
    """Отчет фонда"""
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    fund_id = Column(Integer, ForeignKey("funds.id"), nullable=False)
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    file_url = Column(String(500), nullable=True)
    file_type = Column(String(50), nullable=True)  # pdf, csv, xlsx
    verified = Column(Boolean, default=False)
    total_collected = Column(Numeric(10, 2), nullable=False)
    total_distributed = Column(Numeric(10, 2), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    fund = relationship("Fund", back_populates="reports")


class AnalyticsEvent(Base):
    """События аналитики"""
    __tablename__ = "analytics_events"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    event_type = Column(String(100), nullable=False)  # donation_initiated, subscription_created, etc.
    event_data = Column(JSON, nullable=True)
    session_id = Column(String(255), nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User")
