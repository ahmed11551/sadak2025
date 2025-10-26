import time
import asyncio
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict, deque
import threading
import logging

logger = logging.getLogger(__name__)

@dataclass
class Metric:
    """Базовый класс для метрик"""
    name: str
    value: float
    timestamp: datetime = field(default_factory=datetime.utcnow)
    labels: Dict[str, str] = field(default_factory=dict)

@dataclass
class CounterMetric(Metric):
    """Счетчик"""
    pass

@dataclass
class GaugeMetric(Metric):
    """Измеритель"""
    pass

@dataclass
class HistogramMetric(Metric):
    """Гистограмма"""
    buckets: List[float] = field(default_factory=list)

class MetricsCollector:
    """Сборщик метрик"""
    
    def __init__(self):
        self._counters: Dict[str, float] = defaultdict(float)
        self._gauges: Dict[str, float] = defaultdict(float)
        self._histograms: Dict[str, List[float]] = defaultdict(list)
        self._lock = threading.Lock()
    
    def increment_counter(self, name: str, value: float = 1.0, labels: Dict[str, str] = None):
        """Увеличивает счетчик"""
        with self._lock:
            key = self._make_key(name, labels)
            self._counters[key] += value
    
    def set_gauge(self, name: str, value: float, labels: Dict[str, str] = None):
        """Устанавливает значение измерителя"""
        with self._lock:
            key = self._make_key(name, labels)
            self._gauges[key] = value
    
    def observe_histogram(self, name: str, value: float, labels: Dict[str, str] = None):
        """Добавляет значение в гистограмму"""
        with self._lock:
            key = self._make_key(name, labels)
            self._histograms[key].append(value)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Получает все метрики"""
        with self._lock:
            return {
                'counters': dict(self._counters),
                'gauges': dict(self._gauges),
                'histograms': {
                    name: {
                        'values': values,
                        'count': len(values),
                        'sum': sum(values),
                        'avg': sum(values) / len(values) if values else 0,
                        'min': min(values) if values else 0,
                        'max': max(values) if values else 0
                    }
                    for name, values in self._histograms.items()
                }
            }
    
    def _make_key(self, name: str, labels: Dict[str, str] = None) -> str:
        """Создает ключ для метрики"""
        if not labels:
            return name
        
        label_str = ','.join(f"{k}={v}" for k, v in sorted(labels.items()))
        return f"{name}{{{label_str}}}"

class APIMetrics:
    """Метрики для API"""
    
    def __init__(self, collector: MetricsCollector):
        self.collector = collector
    
    def record_request(self, method: str, endpoint: str, status_code: int, duration: float):
        """Записывает метрики запроса"""
        labels = {
            'method': method,
            'endpoint': endpoint,
            'status_code': str(status_code)
        }
        
        # Счетчик запросов
        self.collector.increment_counter('api_requests_total', labels=labels)
        
        # Длительность запроса
        self.collector.observe_histogram('api_request_duration_seconds', duration, labels=labels)
        
        # Метрики по статус кодам
        status_labels = {'status_code': str(status_code)}
        self.collector.increment_counter('api_responses_total', labels=status_labels)
    
    def record_error(self, method: str, endpoint: str, error_type: str):
        """Записывает метрики ошибок"""
        labels = {
            'method': method,
            'endpoint': endpoint,
            'error_type': error_type
        }
        self.collector.increment_counter('api_errors_total', labels=labels)
    
    def record_rate_limit(self, endpoint: str, limit: int):
        """Записывает метрики превышения лимитов"""
        labels = {
            'endpoint': endpoint,
            'limit': str(limit)
        }
        self.collector.increment_counter('api_rate_limit_exceeded_total', labels=labels)

class BusinessMetrics:
    """Метрики для бизнес-логики"""
    
    def __init__(self, collector: MetricsCollector):
        self.collector = collector
    
    def record_donation(self, amount: float, currency: str, fund_id: int, status: str):
        """Записывает метрики пожертвований"""
        labels = {
            'currency': currency,
            'fund_id': str(fund_id),
            'status': status
        }
        
        self.collector.increment_counter('donations_total', labels=labels)
        self.collector.observe_histogram('donation_amount', amount, labels={'currency': currency})
    
    def record_subscription(self, plan_id: int, status: str):
        """Записывает метрики подписок"""
        labels = {
            'plan_id': str(plan_id),
            'status': status
        }
        self.collector.increment_counter('subscriptions_total', labels=labels)
    
    def record_campaign(self, category: str, status: str):
        """Записывает метрики кампаний"""
        labels = {
            'category': category,
            'status': status
        }
        self.collector.increment_counter('campaigns_total', labels=labels)
    
    def record_zakat_calculation(self, above_nisab: bool):
        """Записывает метрики расчетов закята"""
        labels = {
            'above_nisab': str(above_nisab)
        }
        self.collector.increment_counter('zakat_calculations_total', labels=labels)

class DatabaseMetrics:
    """Метрики для базы данных"""
    
    def __init__(self, collector: MetricsCollector):
        self.collector = collector
    
    def record_query(self, query_type: str, duration: float, success: bool):
        """Записывает метрики запросов к БД"""
        labels = {
            'query_type': query_type,
            'success': str(success)
        }
        
        self.collector.increment_counter('database_queries_total', labels=labels)
        self.collector.observe_histogram('database_query_duration_seconds', duration, labels=labels)
    
    def record_connection(self, status: str):
        """Записывает метрики подключений к БД"""
        labels = {'status': status}
        self.collector.increment_counter('database_connections_total', labels=labels)
    
    def set_connection_pool_size(self, size: int):
        """Устанавливает размер пула подключений"""
        self.collector.set_gauge('database_connection_pool_size', size)

class ExternalServiceMetrics:
    """Метрики для внешних сервисов"""
    
    def __init__(self, collector: MetricsCollector):
        self.collector = collector
    
    def record_api_call(self, service: str, endpoint: str, duration: float, status_code: int):
        """Записывает метрики вызовов внешних API"""
        labels = {
            'service': service,
            'endpoint': endpoint,
            'status_code': str(status_code)
        }
        
        self.collector.increment_counter('external_api_calls_total', labels=labels)
        self.collector.observe_histogram('external_api_duration_seconds', duration, labels=labels)
    
    def record_payment(self, provider: str, amount: float, currency: str, status: str):
        """Записывает метрики платежей"""
        labels = {
            'provider': provider,
            'currency': currency,
            'status': status
        }
        
        self.collector.increment_counter('payments_total', labels=labels)
        self.collector.observe_histogram('payment_amount', amount, labels={'currency': currency})

class SystemMetrics:
    """Системные метрики"""
    
    def __init__(self, collector: MetricsCollector):
        self.collector = collector
    
    def record_memory_usage(self, usage_mb: float):
        """Записывает использование памяти"""
        self.collector.set_gauge('system_memory_usage_mb', usage_mb)
    
    def record_cpu_usage(self, usage_percent: float):
        """Записывает использование CPU"""
        self.collector.set_gauge('system_cpu_usage_percent', usage_percent)
    
    def record_disk_usage(self, usage_percent: float):
        """Записывает использование диска"""
        self.collector.set_gauge('system_disk_usage_percent', usage_percent)
    
    def record_active_connections(self, count: int):
        """Записывает количество активных подключений"""
        self.collector.set_gauge('system_active_connections', count)

class HealthChecker:
    """Проверка здоровья системы"""
    
    def __init__(self):
        self.checks: Dict[str, callable] = {}
        self.results: Dict[str, Dict[str, Any]] = {}
    
    def register_check(self, name: str, check_func: callable):
        """Регистрирует проверку здоровья"""
        self.checks[name] = check_func
    
    async def run_checks(self) -> Dict[str, Any]:
        """Запускает все проверки"""
        results = {}
        
        for name, check_func in self.checks.items():
            try:
                start_time = time.time()
                
                if asyncio.iscoroutinefunction(check_func):
                    result = await check_func()
                else:
                    result = check_func()
                
                duration = time.time() - start_time
                
                results[name] = {
                    'status': 'healthy' if result else 'unhealthy',
                    'duration': duration,
                    'timestamp': datetime.utcnow().isoformat()
                }
                
            except Exception as e:
                results[name] = {
                    'status': 'error',
                    'error': str(e),
                    'timestamp': datetime.utcnow().isoformat()
                }
        
        self.results = results
        return results
    
    def get_overall_status(self) -> str:
        """Получает общий статус системы"""
        if not self.results:
            return 'unknown'
        
        for result in self.results.values():
            if result['status'] != 'healthy':
                return 'unhealthy'
        
        return 'healthy'

class MetricsExporter:
    """Экспортер метрик"""
    
    def __init__(self, collector: MetricsCollector):
        self.collector = collector
    
    def export_prometheus(self) -> str:
        """Экспортирует метрики в формате Prometheus"""
        metrics = self.collector.get_metrics()
        lines = []
        
        # Счетчики
        for name, value in metrics['counters'].items():
            lines.append(f"# TYPE {name} counter")
            lines.append(f"{name} {value}")
        
        # Измерители
        for name, value in metrics['gauges'].items():
            lines.append(f"# TYPE {name} gauge")
            lines.append(f"{name} {value}")
        
        # Гистограммы
        for name, data in metrics['histograms'].items():
            lines.append(f"# TYPE {name} histogram")
            lines.append(f"{name}_count {data['count']}")
            lines.append(f"{name}_sum {data['sum']}")
            lines.append(f"{name}_avg {data['avg']}")
            lines.append(f"{name}_min {data['min']}")
            lines.append(f"{name}_max {data['max']}")
        
        return '\n'.join(lines)
    
    def export_json(self) -> Dict[str, Any]:
        """Экспортирует метрики в формате JSON"""
        return {
            'timestamp': datetime.utcnow().isoformat(),
            'metrics': self.collector.get_metrics()
        }

# Глобальные экземпляры
collector = MetricsCollector()
api_metrics = APIMetrics(collector)
business_metrics = BusinessMetrics(collector)
database_metrics = DatabaseMetrics(collector)
external_service_metrics = ExternalServiceMetrics(collector)
system_metrics = SystemMetrics(collector)
health_checker = HealthChecker()
metrics_exporter = MetricsExporter(collector)

# Декоратор для измерения времени выполнения
def measure_time(metric_name: str, labels: Dict[str, str] = None):
    """Декоратор для измерения времени выполнения функции"""
    def decorator(func):
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                duration = time.time() - start_time
                collector.observe_histogram(metric_name, duration, labels)
                return result
            except Exception as e:
                duration = time.time() - start_time
                collector.observe_histogram(f"{metric_name}_error", duration, labels)
                raise
        
        def sync_wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                collector.observe_histogram(metric_name, duration, labels)
                return result
            except Exception as e:
                duration = time.time() - start_time
                collector.observe_histogram(f"{metric_name}_error", duration, labels)
                raise
        
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator
