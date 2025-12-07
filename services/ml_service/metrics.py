# services/ml_service/metrics.py
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from prometheus_client import CONTENT_TYPE_LATEST
import time

# Метрики
PREDICTION_REQUESTS = Counter(
    'ml_service_prediction_requests_total',
    'Total number of prediction requests'
)

PREDICTION_LATENCY = Histogram(
    'ml_service_prediction_latency_seconds',
    'Prediction latency in seconds',
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0]
)

PREDICTION_VALUE = Histogram(
    'ml_service_prediction_value',
    'Prediction values distribution',
    buckets=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
)

ERROR_REQUESTS_4XX = Counter(
    'ml_service_error_requests_4xx_total',
    'Total number of 4xx error requests'
)

ERROR_REQUESTS_5XX = Counter(
    'ml_service_error_requests_5xx_total',
    'Total number of 5xx error requests'
)

SERVICE_STATUS = Gauge(
    'ml_service_status',
    'Service status (1=healthy, 0=unhealthy)'
)

ACTIVE_REQUESTS = Gauge(
    'ml_service_active_requests',
    'Number of active requests'
)