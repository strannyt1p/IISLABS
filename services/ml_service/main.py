# В начале файла добавьте
from metrics import (
    PREDICTION_REQUESTS, PREDICTION_LATENCY, PREDICTION_VALUE,
    ERROR_REQUESTS_4XX, ERROR_REQUESTS_5XX, SERVICE_STATUS, ACTIVE_REQUESTS,
    generate_latest, CONTENT_TYPE_LATEST
)
from starlette.responses import Response

# Добавьте endpoint для метрик
@app.get("/metrics")
def get_metrics():
    """Endpoint для Prometheus метрик"""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

# Обновите health endpoint для метрик
@app.get("/health")
def health_check():
    """Проверка статуса сервиса и модели"""
    if api_handler is None:
        SERVICE_STATUS.set(0)
        raise HTTPException(status_code=500, detail="Модель не загружена")
    
    SERVICE_STATUS.set(1)
    return {"status": "healthy", "model_loaded": True}

# Обновите prediction endpoint с метриками
@app.post("/api/prediction/{item_id}", response_model=PredictionResponse)
def make_prediction(item_id: int, request: PredictionRequest):
    PREDICTION_REQUESTS.inc()
    ACTIVE_REQUESTS.inc()
    
    start_time = time.time()
    
    if api_handler is None:
        ERROR_REQUESTS_5XX.inc()
        ACTIVE_REQUESTS.dec()
        raise HTTPException(status_code=500, detail="Модель не доступна")
    
    try:
        prediction = api_handler.predict(request.features)
        
        # Записываем метрики
        latency = time.time() - start_time
        PREDICTION_LATENCY.observe(latency)
        PREDICTION_VALUE.observe(prediction)
        
        ACTIVE_REQUESTS.dec()
        return PredictionResponse(item_id=item_id, price=prediction)
        
    except HTTPException as e:
        if 400 <= e.status_code < 500:
            ERROR_REQUESTS_4XX.inc()
        elif 500 <= e.status_code < 600:
            ERROR_REQUESTS_5XX.inc()
        ACTIVE_REQUESTS.dec()
        raise e
    except Exception as e:
        ERROR_REQUESTS_5XX.inc()
        ACTIVE_REQUESTS.dec()
        raise HTTPException(status_code=500, detail=f"Ошибка предсказания: {str(e)}")