from elasticsearch import Elasticsearch
from typing import List, Dict, Any, Optional
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ElasticsearchService:
    """Сервис для работы с Elasticsearch"""
    
    def __init__(self, elasticsearch_url: str):
        self.client = Elasticsearch([elasticsearch_url])
        self.index_prefix = "sadaka_pass"
        
    def create_indices(self):
        """Создание индексов для всех типов данных"""
        self._create_funds_index()
        self._create_campaigns_index()
        self._create_users_index()
        
    def _create_funds_index(self):
        """Создание индекса для фондов"""
        index_name = f"{self.index_prefix}_funds"
        
        mapping = {
            "mappings": {
                "properties": {
                    "id": {"type": "integer"},
                    "name": {
                        "type": "text",
                        "analyzer": "russian",
                        "fields": {
                            "keyword": {"type": "keyword"}
                        }
                    },
                    "description": {
                        "type": "text",
                        "analyzer": "russian"
                    },
                    "country_code": {"type": "keyword"},
                    "purposes": {"type": "keyword"},
                    "verified": {"type": "boolean"},
                    "active": {"type": "boolean"},
                    "partner_enabled": {"type": "boolean"},
                    "website": {"type": "keyword"},
                    "created_at": {"type": "date"},
                    "updated_at": {"type": "date"}
                }
            },
            "settings": {
                "analysis": {
                    "analyzer": {
                        "russian": {
                            "type": "custom",
                            "tokenizer": "standard",
                            "filter": [
                                "lowercase",
                                "russian_stop",
                                "russian_stemmer"
                            ]
                        }
                    },
                    "filter": {
                        "russian_stop": {
                            "type": "stop",
                            "stopwords": "_russian_"
                        },
                        "russian_stemmer": {
                            "type": "stemmer",
                            "language": "russian"
                        }
                    }
                }
            }
        }
        
        if not self.client.indices.exists(index=index_name):
            self.client.indices.create(index=index_name, body=mapping)
            logger.info(f"Created index: {index_name}")
    
    def _create_campaigns_index(self):
        """Создание индекса для кампаний"""
        index_name = f"{self.index_prefix}_campaigns"
        
        mapping = {
            "mappings": {
                "properties": {
                    "id": {"type": "integer"},
                    "title": {
                        "type": "text",
                        "analyzer": "russian",
                        "fields": {
                            "keyword": {"type": "keyword"}
                        }
                    },
                    "description": {
                        "type": "text",
                        "analyzer": "russian"
                    },
                    "category": {"type": "keyword"},
                    "goal_amount": {"type": "float"},
                    "collected_amount": {"type": "float"},
                    "country_code": {"type": "keyword"},
                    "status": {"type": "keyword"},
                    "owner_id": {"type": "integer"},
                    "fund_id": {"type": "integer"},
                    "end_date": {"type": "date"},
                    "created_at": {"type": "date"},
                    "updated_at": {"type": "date"}
                }
            },
            "settings": {
                "analysis": {
                    "analyzer": {
                        "russian": {
                            "type": "custom",
                            "tokenizer": "standard",
                            "filter": [
                                "lowercase",
                                "russian_stop",
                                "russian_stemmer"
                            ]
                        }
                    },
                    "filter": {
                        "russian_stop": {
                            "type": "stop",
                            "stopwords": "_russian_"
                        },
                        "russian_stemmer": {
                            "type": "stemmer",
                            "language": "russian"
                        }
                    }
                }
            }
        }
        
        if not self.client.indices.exists(index=index_name):
            self.client.indices.create(index=index_name, body=mapping)
            logger.info(f"Created index: {index_name}")
    
    def _create_users_index(self):
        """Создание индекса для пользователей"""
        index_name = f"{self.index_prefix}_users"
        
        mapping = {
            "mappings": {
                "properties": {
                    "id": {"type": "integer"},
                    "telegram_id": {"type": "long"},
                    "username": {"type": "keyword"},
                    "first_name": {
                        "type": "text",
                        "analyzer": "russian"
                    },
                    "last_name": {
                        "type": "text",
                        "analyzer": "russian"
                    },
                    "language_code": {"type": "keyword"},
                    "locale": {"type": "keyword"},
                    "is_premium": {"type": "boolean"},
                    "is_active": {"type": "boolean"},
                    "created_at": {"type": "date"},
                    "updated_at": {"type": "date"}
                }
            }
        }
        
        if not self.client.indices.exists(index=index_name):
            self.client.indices.create(index=index_name, body=mapping)
            logger.info(f"Created index: {index_name}")
    
    def index_fund(self, fund_data: Dict[str, Any]) -> bool:
        """Индексация фонда"""
        try:
            index_name = f"{self.index_prefix}_funds"
            self.client.index(
                index=index_name,
                id=fund_data["id"],
                body=fund_data
            )
            logger.info(f"Indexed fund: {fund_data['id']}")
            return True
        except Exception as e:
            logger.error(f"Error indexing fund {fund_data.get('id')}: {e}")
            return False
    
    def index_campaign(self, campaign_data: Dict[str, Any]) -> bool:
        """Индексация кампании"""
        try:
            index_name = f"{self.index_prefix}_campaigns"
            self.client.index(
                index=index_name,
                id=campaign_data["id"],
                body=campaign_data
            )
            logger.info(f"Indexed campaign: {campaign_data['id']}")
            return True
        except Exception as e:
            logger.error(f"Error indexing campaign {campaign_data.get('id')}: {e}")
            return False
    
    def index_user(self, user_data: Dict[str, Any]) -> bool:
        """Индексация пользователя"""
        try:
            index_name = f"{self.index_prefix}_users"
            self.client.index(
                index=index_name,
                id=user_data["id"],
                body=user_data
            )
            logger.info(f"Indexed user: {user_data['id']}")
            return True
        except Exception as e:
            logger.error(f"Error indexing user {user_data.get('id')}: {e}")
            return False
    
    def search_funds(
        self, 
        query: str = "", 
        country_code: Optional[str] = None,
        purposes: Optional[List[str]] = None,
        verified_only: bool = False,
        size: int = 20,
        from_: int = 0
    ) -> Dict[str, Any]:
        """Поиск фондов"""
        index_name = f"{self.index_prefix}_funds"
        
        # Базовый запрос
        search_body = {
            "query": {
                "bool": {
                    "must": [],
                    "filter": []
                }
            },
            "size": size,
            "from": from_,
            "sort": [
                {"verified": {"order": "desc"}},
                {"created_at": {"order": "desc"}}
            ]
        }
        
        # Текстовый поиск
        if query:
            search_body["query"]["bool"]["must"].append({
                "multi_match": {
                    "query": query,
                    "fields": ["name^2", "description"],
                    "type": "best_fields",
                    "fuzziness": "AUTO"
                }
            })
        else:
            search_body["query"]["bool"]["must"].append({"match_all": {}})
        
        # Фильтры
        filters = []
        
        if country_code:
            filters.append({"term": {"country_code": country_code}})
        
        if purposes:
            filters.append({"terms": {"purposes": purposes}})
        
        if verified_only:
            filters.append({"term": {"verified": True}})
        
        # Только активные фонды
        filters.append({"term": {"active": True}})
        
        if filters:
            search_body["query"]["bool"]["filter"] = filters
        
        try:
            response = self.client.search(index=index_name, body=search_body)
            return {
                "hits": response["hits"]["hits"],
                "total": response["hits"]["total"]["value"],
                "took": response["took"]
            }
        except Exception as e:
            logger.error(f"Error searching funds: {e}")
            return {"hits": [], "total": 0, "took": 0}
    
    def search_campaigns(
        self,
        query: str = "",
        category: Optional[str] = None,
        country_code: Optional[str] = None,
        status: str = "active",
        size: int = 20,
        from_: int = 0
    ) -> Dict[str, Any]:
        """Поиск кампаний"""
        index_name = f"{self.index_prefix}_campaigns"
        
        search_body = {
            "query": {
                "bool": {
                    "must": [],
                    "filter": []
                }
            },
            "size": size,
            "from": from_,
            "sort": [
                {"created_at": {"order": "desc"}}
            ]
        }
        
        # Текстовый поиск
        if query:
            search_body["query"]["bool"]["must"].append({
                "multi_match": {
                    "query": query,
                    "fields": ["title^2", "description"],
                    "type": "best_fields",
                    "fuzziness": "AUTO"
                }
            })
        else:
            search_body["query"]["bool"]["must"].append({"match_all": {}})
        
        # Фильтры
        filters = []
        
        if category:
            filters.append({"term": {"category": category}})
        
        if country_code:
            filters.append({"term": {"country_code": country_code}})
        
        if status:
            filters.append({"term": {"status": status}})
        
        if filters:
            search_body["query"]["bool"]["filter"] = filters
        
        try:
            response = self.client.search(index=index_name, body=search_body)
            return {
                "hits": response["hits"]["hits"],
                "total": response["hits"]["total"]["value"],
                "took": response["took"]
            }
        except Exception as e:
            logger.error(f"Error searching campaigns: {e}")
            return {"hits": [], "total": 0, "took": 0}
    
    def search_users(
        self,
        query: str = "",
        is_premium: Optional[bool] = None,
        is_active: Optional[bool] = None,
        size: int = 20,
        from_: int = 0
    ) -> Dict[str, Any]:
        """Поиск пользователей"""
        index_name = f"{self.index_prefix}_users"
        
        search_body = {
            "query": {
                "bool": {
                    "must": [],
                    "filter": []
                }
            },
            "size": size,
            "from": from_,
            "sort": [
                {"created_at": {"order": "desc"}}
            ]
        }
        
        # Текстовый поиск
        if query:
            search_body["query"]["bool"]["must"].append({
                "multi_match": {
                    "query": query,
                    "fields": ["first_name^2", "last_name", "username"],
                    "type": "best_fields",
                    "fuzziness": "AUTO"
                }
            })
        else:
            search_body["query"]["bool"]["must"].append({"match_all": {}})
        
        # Фильтры
        filters = []
        
        if is_premium is not None:
            filters.append({"term": {"is_premium": is_premium}})
        
        if is_active is not None:
            filters.append({"term": {"is_active": is_active}})
        
        if filters:
            search_body["query"]["bool"]["filter"] = filters
        
        try:
            response = self.client.search(index=index_name, body=search_body)
            return {
                "hits": response["hits"]["hits"],
                "total": response["hits"]["total"]["value"],
                "took": response["took"]
            }
        except Exception as e:
            logger.error(f"Error searching users: {e}")
            return {"hits": [], "total": 0, "took": 0}
    
    def delete_document(self, index_type: str, doc_id: int) -> bool:
        """Удаление документа из индекса"""
        try:
            index_name = f"{self.index_prefix}_{index_type}"
            self.client.delete(index=index_name, id=doc_id)
            logger.info(f"Deleted {index_type}: {doc_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting {index_type} {doc_id}: {e}")
            return False
    
    def update_document(self, index_type: str, doc_id: int, doc_data: Dict[str, Any]) -> bool:
        """Обновление документа в индексе"""
        try:
            index_name = f"{self.index_prefix}_{index_type}"
            self.client.index(
                index=index_name,
                id=doc_id,
                body=doc_data
            )
            logger.info(f"Updated {index_type}: {doc_id}")
            return True
        except Exception as e:
            logger.error(f"Error updating {index_type} {doc_id}: {e}")
            return False
    
    def get_analytics(self, index_type: str, date_from: str, date_to: str) -> Dict[str, Any]:
        """Получение аналитики по индексу"""
        index_name = f"{self.index_prefix}_{index_type}"
        
        search_body = {
            "query": {
                "range": {
                    "created_at": {
                        "gte": date_from,
                        "lte": date_to
                    }
                }
            },
            "aggs": {
                "daily_stats": {
                    "date_histogram": {
                        "field": "created_at",
                        "calendar_interval": "day"
                    }
                },
                "total_count": {
                    "value_count": {
                        "field": "id"
                    }
                }
            },
            "size": 0
        }
        
        try:
            response = self.client.search(index=index_name, body=search_body)
            return {
                "daily_stats": response["aggregations"]["daily_stats"]["buckets"],
                "total_count": response["aggregations"]["total_count"]["value"]
            }
        except Exception as e:
            logger.error(f"Error getting analytics for {index_type}: {e}")
            return {"daily_stats": [], "total_count": 0}
    
    def health_check(self) -> Dict[str, Any]:
        """Проверка состояния Elasticsearch"""
        try:
            health = self.client.cluster.health()
            return {
                "status": health["status"],
                "cluster_name": health["cluster_name"],
                "number_of_nodes": health["number_of_nodes"],
                "active_shards": health["active_shards"]
            }
        except Exception as e:
            logger.error(f"Elasticsearch health check failed: {e}")
            return {"status": "red", "error": str(e)}
