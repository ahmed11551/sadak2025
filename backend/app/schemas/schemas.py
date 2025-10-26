from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


# User Schemas
class UserBase(BaseModel):
    telegram_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    language_code: str = "ru"
    locale: str = "ru"
    timezone: str = "UTC"
    madhab: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    language_code: Optional[str] = None
    locale: Optional[str] = None
    timezone: Optional[str] = None
    madhab: Optional[str] = None


class User(UserBase):
    id: int
    is_premium: bool = False
    is_active: bool = True
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Fund Schemas
class FundBase(BaseModel):
    name: str
    short_desc: Optional[str] = None
    country_code: str
    purposes: Optional[List[str]] = None
    logo_url: Optional[str] = None
    website: Optional[str] = None
    social_links: Optional[dict] = None
    partner_enabled: Optional[bool] = False


class FundCreate(FundBase):
    pass


class FundUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    country_code: Optional[str] = None
    purposes: Optional[List[str]] = None
    logo_url: Optional[str] = None
    website_url: Optional[str] = None
    contact_info: Optional[dict] = None
    verified: Optional[bool] = None
    active: Optional[bool] = None


class Fund(FundBase):
    id: int
    verified: bool = False
    active: bool = True
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Donation Schemas
class DonationBase(BaseModel):
    fund_id: int
    amount: Decimal
    currency: str = "RUB"
    purpose: Optional[str] = None
    payment_method: str


class DonationCreate(DonationBase):
    pass


class DonationUpdate(BaseModel):
    status: Optional[str] = None
    payment_id: Optional[str] = None
    transaction_id: Optional[str] = None


class Donation(DonationBase):
    id: int
    user_id: int
    status: str = "pending"
    payment_id: Optional[str] = None
    transaction_id: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Subscription Schemas
class SubscriptionBase(BaseModel):
    fund_id: int
    amount: Decimal
    currency: str = "RUB"
    frequency: str  # monthly, weekly, daily
    purpose: Optional[str] = None
    payment_method: str


class SubscriptionCreate(SubscriptionBase):
    pass


class SubscriptionUpdate(BaseModel):
    status: Optional[str] = None
    next_payment_date: Optional[datetime] = None


class Subscription(SubscriptionBase):
    id: int
    user_id: int
    subscription_id: Optional[str] = None
    status: str = "active"
    next_payment_date: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Zakat Calculation Schemas
class ZakatCalculationBase(BaseModel):
    cash_at_home: Decimal = 0
    bank_accounts: Decimal = 0
    shares_value: Decimal = 0
    goods_profit: Decimal = 0
    gold_silver_value: Decimal = 0
    property_investments: Decimal = 0
    other_income: Decimal = 0
    debts: Decimal = 0
    expenses: Decimal = 0


class ZakatCalculationCreate(ZakatCalculationBase):
    pass


class ZakatCalculationUpdate(BaseModel):
    is_paid: Optional[bool] = None
    payment_id: Optional[str] = None


class ZakatCalculation(ZakatCalculationBase):
    id: int
    user_id: int
    total_assets: Decimal = 0
    total_liabilities: Decimal = 0
    zakatable_amount: Decimal = 0
    nisab_amount: Decimal = 952389
    zakat_amount: Decimal = 0
    is_paid: bool = False
    payment_id: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Partner Application Schemas
class PartnerApplicationBase(BaseModel):
    organization_name: str
    contact_person: str
    email: EmailStr
    phone: Optional[str] = None
    website: Optional[str] = None
    description: str
    purposes: Optional[List[str]] = None
    documents: Optional[dict] = None


class PartnerApplicationCreate(PartnerApplicationBase):
    pass


class PartnerApplicationUpdate(BaseModel):
    status: Optional[str] = None
    review_notes: Optional[str] = None


class PartnerApplication(PartnerApplicationBase):
    id: int
    status: str = "pending"
    reviewed_by: Optional[int] = None
    review_notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Response Schemas
class MessageResponse(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None


# Campaign Types
class CampaignBase(BaseModel):
    fund_id: Optional[int] = None
    title: str
    description: str
    category: str
    goal_amount: Decimal
    country_code: str
    end_date: Optional[date] = None
    banner_url: Optional[str] = None


class CampaignCreate(CampaignBase):
    pass


class CampaignUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    goal_amount: Optional[Decimal] = None
    end_date: Optional[date] = None
    banner_url: Optional[str] = None
    status: Optional[str] = None


class Campaign(CampaignBase):
    id: int
    owner_id: int
    collected_amount: Decimal = 0
    status: str = "pending"
    participants_count: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Subscription Plan Types
class SubscriptionPlanBase(BaseModel):
    name: str
    display_name: str
    description: Optional[str] = None
    price_monthly: Decimal
    price_3months: Optional[Decimal] = None
    price_6months: Optional[Decimal] = None
    price_12months: Optional[Decimal] = None
    charity_percentage: Decimal = 0
    features: Optional[List[str]] = None


class SubscriptionPlanCreate(SubscriptionPlanBase):
    pass


class SubscriptionPlanUpdate(BaseModel):
    display_name: Optional[str] = None
    description: Optional[str] = None
    price_monthly: Optional[Decimal] = None
    price_3months: Optional[Decimal] = None
    price_6months: Optional[Decimal] = None
    price_12months: Optional[Decimal] = None
    charity_percentage: Optional[Decimal] = None
    features: Optional[List[str]] = None
    is_active: Optional[bool] = None


class SubscriptionPlan(SubscriptionPlanBase):
    id: int
    is_active: bool = True
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Report Types
class ReportBase(BaseModel):
    fund_id: int
    period_start: date
    period_end: date
    file_url: Optional[str] = None
    file_type: Optional[str] = None
    total_collected: Decimal
    total_distributed: Decimal
    description: Optional[str] = None


class ReportCreate(ReportBase):
    pass


class ReportUpdate(BaseModel):
    file_url: Optional[str] = None
    file_type: Optional[str] = None
    total_collected: Optional[Decimal] = None
    total_distributed: Optional[Decimal] = None
    description: Optional[str] = None
    verified: Optional[bool] = None


class Report(ReportBase):
    id: int
    verified: bool = False
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Analytics Event Types
class AnalyticsEventBase(BaseModel):
    event_type: str
    event_data: Optional[dict] = None
    session_id: Optional[str] = None


class AnalyticsEventCreate(AnalyticsEventBase):
    user_id: Optional[int] = None


class AnalyticsEvent(AnalyticsEventBase):
    id: int
    user_id: Optional[int] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
