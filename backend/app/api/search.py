from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import logging

from ..core.database import get_db
from ..services.elasticsearch_service import ElasticsearchService
from ..core.config import get_settings

logger = logging.getLogger(__name__)
router = APIRouter()

# Инициализация Elasticsearch сервиса
settings = get_settings()
es_service = ElasticsearchService(settings.elasticsearch_url)

@router.get("/funds/search", response_model=Dict[str, Any])
def search_funds(
    q: str = Query("", description="Поисковый запрос"),
    country_code: Optional[str] = Query(None, description="Код страны"),
    purposes: Optional[str] = Query(None, description="Цели фонда (через запятую)"),
    verified_only: bool = Query(False, description="Только верифицированные фонды"),
    size: int = Query(20, ge=1, le=100, description="Количество результатов"),
    from_: int = Query(0, ge=0, description="Смещение"),
    db: Session = Depends(get_db)
):
    """Поиск фондов через Elasticsearch"""
    try:
        # Парсим цели
        purposes_list = None
        if purposes:
            purposes_list = [p.strip() for p in purposes.split(",")]
        
        # Выполняем поиск
        results = es_service.search_funds(
            query=q,
            country_code=country_code,
            purposes=purposes_list,
            verified_only=verified_only,
            size=size,
            from_=from_
        )
        
        # Форматируем результаты
        formatted_results = []
        for hit in results["hits"]:
            fund_data = hit["_source"]
            fund_data["_score"] = hit["_score"]
            formatted_results.append(fund_data)
        
        return {
            "results": formatted_results,
            "total": results["total"],
            "took": results["took"],
            "query": {
                "text": q,
                "country_code": country_code,
                "purposes": purposes_list,
                "verified_only": verified_only
            }
        }
        
    except Exception as e:
        logger.error(f"Error in fund search: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка поиска фондов"
        )

@router.get("/campaigns/search", response_model=Dict[str, Any])
def search_campaigns(
    q: str = Query("", description="Поисковый запрос"),
    category: Optional[str] = Query(None, description="Категория кампании"),
    country_code: Optional[str] = Query(None, description="Код страны"),
    status: str = Query("active", description="Статус кампании"),
    size: int = Query(20, ge=1, le=100, description="Количество результатов"),
    from_: int = Query(0, ge=0, description="Смещение"),
    db: Session = Depends(get_db)
):
    """Поиск кампаний через Elasticsearch"""
    try:
        # Выполняем поиск
        results = es_service.search_campaigns(
            query=q,
            category=category,
            country_code=country_code,
            status=status,
            size=size,
            from_=from_
        )
        
        # Форматируем результаты
        formatted_results = []
        for hit in results["hits"]:
            campaign_data = hit["_source"]
            campaign_data["_score"] = hit["_score"]
            formatted_results.append(campaign_data)
        
        return {
            "results": formatted_results,
            "total": results["total"],
            "took": results["took"],
            "query": {
                "text": q,
                "category": category,
                "country_code": country_code,
                "status": status
            }
        }
        
    except Exception as e:
        logger.error(f"Error in campaign search: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка поиска кампаний"
        )

@router.get("/users/search", response_model=Dict[str, Any])
def search_users(
    q: str = Query("", description="Поисковый запрос"),
    is_premium: Optional[bool] = Query(None, description="Premium статус"),
    is_active: Optional[bool] = Query(None, description="Активность"),
    size: int = Query(20, ge=1, le=100, description="Количество результатов"),
    from_: int = Query(0, ge=0, description="Смещение"),
    db: Session = Depends(get_db)
):
    """Поиск пользователей через Elasticsearch"""
    try:
        # Выполняем поиск
        results = es_service.search_users(
            query=q,
            is_premium=is_premium,
            is_active=is_active,
            size=size,
            from_=from_
        )
        
        # Форматируем результаты
        formatted_results = []
        for hit in results["hits"]:
            user_data = hit["_source"]
            user_data["_score"] = hit["_score"]
            formatted_results.append(user_data)
        
        return {
            "results": formatted_results,
            "total": results["total"],
            "took": results["took"],
            "query": {
                "text": q,
                "is_premium": is_premium,
                "is_active": is_active
            }
        }
        
    except Exception as e:
        logger.error(f"Error in user search: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка поиска пользователей"
        )

@router.post("/index/fund/{fund_id}")
def index_fund(fund_id: int, db: Session = Depends(get_db)):
    """Индексация фонда в Elasticsearch"""
    try:
        # Получаем данные фонда из БД
        from ..models.models import Fund
        fund = db.query(Fund).filter(Fund.id == fund_id).first()
        
        if not fund:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Фонд не найден"
            )
        
        # Подготавливаем данные для индексации
        fund_data = {
            "id": fund.id,
            "name": fund.name,
            "description": fund.short_desc or "",
            "country_code": fund.country_code,
            "purposes": fund.purposes or [],
            "verified": fund.verified,
            "active": fund.active,
            "partner_enabled": fund.partner_enabled,
            "website": fund.website,
            "created_at": fund.created_at.isoformat() if fund.created_at else None,
            "updated_at": fund.updated_at.isoformat() if fund.updated_at else None
        }
        
        # Индексируем
        success = es_service.index_fund(fund_data)
        
        if success:
            return {"message": f"Фонд {fund_id} успешно проиндексирован"}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка индексации фонда"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error indexing fund {fund_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка индексации фонда"
        )

@router.post("/index/campaign/{campaign_id}")
def index_campaign(campaign_id: int, db: Session = Depends(get_db)):
    """Индексация кампании в Elasticsearch"""
    try:
        # Получаем данные кампании из БД
        from ..models.models import Campaign
        campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
        
        if not campaign:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Кампания не найдена"
            )
        
        # Подготавливаем данные для индексации
        campaign_data = {
            "id": campaign.id,
            "title": campaign.title,
            "description": campaign.description,
            "category": campaign.category,
            "goal_amount": float(campaign.goal_amount),
            "collected_amount": float(campaign.collected_amount),
            "country_code": campaign.country_code,
            "status": campaign.status,
            "owner_id": campaign.owner_id,
            "fund_id": campaign.fund_id,
            "end_date": campaign.end_date.isoformat() if campaign.end_date else None,
            "created_at": campaign.created_at.isoformat() if campaign.created_at else None,
            "updated_at": campaign.updated_at.isoformat() if campaign.updated_at else None
        }
        
        # Индексируем
        success = es_service.index_campaign(campaign_data)
        
        if success:
            return {"message": f"Кампания {campaign_id} успешно проиндексирована"}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка индексации кампании"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error indexing campaign {campaign_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка индексации кампании"
        )

@router.get("/health")
def elasticsearch_health():
    """Проверка состояния Elasticsearch"""
    try:
        health = es_service.health_check()
        return health
    except Exception as e:
        logger.error(f"Elasticsearch health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Elasticsearch недоступен"
        )

@router.post("/reindex/all")
def reindex_all(db: Session = Depends(get_db)):
    """Полная переиндексация всех данных"""
    try:
        # Создаем индексы
        es_service.create_indices()
        
        # Переиндексируем фонды
        from ..models.models import Fund
        funds = db.query(Fund).all()
        funds_indexed = 0
        
        for fund in funds:
            fund_data = {
                "id": fund.id,
                "name": fund.name,
                "description": fund.short_desc or "",
                "country_code": fund.country_code,
                "purposes": fund.purposes or [],
                "verified": fund.verified,
                "active": fund.active,
                "partner_enabled": fund.partner_enabled,
                "website": fund.website,
                "created_at": fund.created_at.isoformat() if fund.created_at else None,
                "updated_at": fund.updated_at.isoformat() if fund.updated_at else None
            }
            if es_service.index_fund(fund_data):
                funds_indexed += 1
        
        # Переиндексируем кампании
        from ..models.models import Campaign
        campaigns = db.query(Campaign).all()
        campaigns_indexed = 0
        
        for campaign in campaigns:
            campaign_data = {
                "id": campaign.id,
                "title": campaign.title,
                "description": campaign.description,
                "category": campaign.category,
                "goal_amount": float(campaign.goal_amount),
                "collected_amount": float(campaign.collected_amount),
                "country_code": campaign.country_code,
                "status": campaign.status,
                "owner_id": campaign.owner_id,
                "fund_id": campaign.fund_id,
                "end_date": campaign.end_date.isoformat() if campaign.end_date else None,
                "created_at": campaign.created_at.isoformat() if campaign.created_at else None,
                "updated_at": campaign.updated_at.isoformat() if campaign.updated_at else None
            }
            if es_service.index_campaign(campaign_data):
                campaigns_indexed += 1
        
        return {
            "message": "Переиндексация завершена",
            "funds_indexed": funds_indexed,
            "campaigns_indexed": campaigns_indexed
        }
        
    except Exception as e:
        logger.error(f"Error in full reindex: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка переиндексации"
        )
