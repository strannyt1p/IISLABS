from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Union
import sys
import os

# Добавляем путь к api_handler
sys.path.append(os.path.dirname(__file__))

try:
    from api_handler import FastAPIHandler
except ImportError as e:
    print(f"Import error: {e}")
    FastAPIHandler = None

app = FastAPI()

# Инициализация обработчика с моделью
api_handler = None
try:
    print("Пытаемся инициализировать API Handler...")
    api_handler = FastAPIHandler()
    print("API Handler успешно инициализирован")
except Exception as e:
    print(f"Ошибка при инициализации API Handler: {e}")
    import traceback
    traceback.print_exc()

# Модель данных для входных признаков - используем Union для смешанных типов
class PredictionRequest(BaseModel):
    features: List[Union[float, str, int]]

class PredictionResponse(BaseModel):
    item_id: int
    price: float

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health")
def health_check():
    """Проверка статуса сервиса и модели"""
    if api_handler is None:
        raise HTTPException(status_code=500, detail="Модель не загружена")
    return {"status": "healthy", "model_loaded": True}

@app.post("/api/prediction/{item_id}", response_model=PredictionResponse)
def make_prediction(item_id: int, request: PredictionRequest):
    if api_handler is None:
        raise HTTPException(status_code=500, detail="Модель не доступна")
    
    try:
        # Преобразуем все элементы в правильные типы
        processed_features = []
        for feature in request.features:
            if isinstance(feature, str):
                processed_features.append(feature)
            else:
                processed_features.append(float(feature))
        
        # Получаем предсказание от модели
        prediction = api_handler.predict(processed_features)
        
        return PredictionResponse(
            item_id=item_id,
            price=prediction
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка предсказания: {str(e)}")