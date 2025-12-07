# services/requests/Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY requests.py .

CMD ["python", "requests.py"]

# Команда для сборки образа:
# docker build -t requests_service:1 .

# Команда для запуска контейнера:
# docker run --network host requests_service:1