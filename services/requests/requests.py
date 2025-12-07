# services/requests/requests.py
import requests
import time
import random
import json
from datetime import datetime

# В начале request_sender.py добавьте
import sys
import os
sys.path.remove(os.path.dirname(os.path.abspath(__file__)))
import requests


SERVICE_URL = "http://localhost:8000"  # для локального тестирования
# SERVICE_URL = "http://ml_service:8000"  # для docker compose

# Примеры данных для тестирования
TEST_DATA = [
    [63, 1, 3, 145, 233, 1, 0, 150, 0, 2.3, 0, 0, 1, "60+", "high", 3.7],
    [37, 1, 2, 130, 250, 0, 1, 187, 0, 3.5, 0, 0, 2, "<40", "elevated", 6.8],
    [41, 0, 1, 130, 204, 0, 0, 172, 0, 1.4, 2, 0, 2, "40-50", "elevated", 5.0],
    [56, 1, 1, 120, 236, 0, 1, 178, 0, 0.8, 2, 0, 2, "50-60", "normal", 4.2],
    [57, 0, 0, 120, 354, 0, 1, 163, 1, 0.6, 2, 0, 2, "50-60", "normal", 6.2]
]

def send_request(item_id: int, features: list):
    """Отправка запроса к сервису предсказаний"""
    url = f"{SERVICE_URL}/api/prediction/{item_id}"
    payload = {"features": features}
    
    try:
        start_time = time.time()
        response = requests.post(url, json=payload, timeout=5)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        if response.status_code == 200:
            result = response.json()
            print(f"[{datetime.now()}] ✅ Успех | ID: {result['item_id']} | "
                  f"Предсказание: {result['price']} | Время: {response_time:.3f}с")
            return True
        else:
            print(f"[{datetime.now()}] ❌ Ошибка {response.status_code} | "
                  f"Ответ: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"[{datetime.now()}] ❌ Ошибка соединения: {e}")
        return False
    except Exception as e:
        print(f"[{datetime.now()}] ❌ Неожиданная ошибка: {e}")
        return False

def main():
    """Основная функция отправки запросов"""
    print("=" * 60)
    print("Тестирование сервиса предсказаний")
    print(f"Целевой сервис: {SERVICE_URL}")
    print("=" * 60)
    
    request_count = 0
    success_count = 0
    
    try:
        while True:
            # Выбираем случайные данные
            features = random.choice(TEST_DATA)
            item_id = random.randint(1000, 9999)
            
            # Отправляем запрос
            if send_request(item_id, features):
                success_count += 1
            
            request_count += 1
            
            # Выводим статистику
            if request_count % 10 == 0:
                print("-" * 60)
                print(f"Статистика: {request_count} запросов | "
                      f"Успешно: {success_count} | "
                      f"Успешность: {(success_count/request_count*100):.1f}%")
                print("-" * 60)
            
            # Случайная пауза между запросами (0-5 секунд)
            sleep_time = random.uniform(0, 5)
            time.sleep(sleep_time)
            
    except KeyboardInterrupt:
        print("\n" + "=" * 60)
        print("Тестирование завершено")
        print(f"Итог: {request_count} запросов | "
              f"Успешно: {success_count} | "
              f"Успешность: {(success_count/max(request_count, 1)*100):.1f}%")
        print("=" * 60)

if __name__ == "__main__":
    main()