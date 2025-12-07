# services/models/create_simple_model.py
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import numpy as np

print("Создаем простую совместимую модель...")

# Простые данные для обучения
np.random.seed(42)
n_samples = 100

# Генерируем синтетические данные с 16 признаками
X = np.random.randn(n_samples, 16)
y = np.random.randint(0, 2, n_samples)

# Простая модель
model = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', RandomForestClassifier(n_estimators=10, random_state=42))
])

print("Обучаем модель...")
model.fit(X, y)

# Сохраняем
print("Сохраняем модель...")
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✅ Модель создана и сохранена как model.pkl")
print(f"Точность на обучающих данных: {model.score(X, y):.3f}")