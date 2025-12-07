# Используем официальный Python образ
FROM python:3.10-slim

# Копируем содержимое текущей директории в /ml_service в контейнере
COPY . /ml_service

# Создаем директорию для моделей и делаем ее доступной снаружи
RUN mkdir -p /models
VOLUME /models

# Устанавливаем рабочую директорию
WORKDIR /ml_service

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт 8000
EXPOSE 8000

# Запускаем сервер
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Команда для сборки образа:
# docker build -t ml_service:1 .

# Команда для запуска контейнера:
# docker run -p 8000:8000 -v $(pwd)/../models:/models ml_service:1