import pickle
import pandas as pd
import os

class FastAPIHandler:
    def __init__(self, model_path: str = "/models/model.pkl"):

        """
        Инициализация обработчика - загрузка модели
        """
        self.model_path = model_path
        self.model = self._load_model()
        self.feature_names = [
            'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 
            'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 
            'age_group', 'bp_category', 'chol_age_ratio'
        ]
        print(f"Модель ожидает признаки: {self.feature_names}")
    
    def _load_model(self):
        """
        Загрузка модели из файла
        """
        try:
            with open(self.model_path, 'rb') as f:
                model = pickle.load(f)
            print("Модель успешно загружена")
            return model
        except Exception as e:
            print(f"Ошибка при загрузке модели: {e}")
            raise e
    
    def predict(self, features: list) -> float:
        """
        Выполнение предсказания на основе признаков
        Вся логика проверки и преобразования здесь
        """
        try:
            # Проверяем количество признаков
            if len(features) != len(self.feature_names):
                raise ValueError(f"Ожидается {len(self.feature_names)} признаков, получено {len(features)}")
            
            # Преобразуем и проверяем каждый признак
            processed_features = []
            for i, (feature_name, feature_value) in enumerate(zip(self.feature_names, features)):
                try:
                    if feature_name in ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 
                                       'thalach', 'exang', 'slope', 'ca', 'thal']:
                        # Целочисленные признаки
                        processed_features.append(int(float(feature_value)))
                    elif feature_name in ['oldpeak', 'chol_age_ratio']:
                        # Числа с плавающей точкой
                        processed_features.append(float(feature_value))
                    else:  # строковые признаки: age_group, bp_category
                        processed_features.append(str(feature_value))
                except (ValueError, TypeError) as e:
                    raise ValueError(f"Неверный тип для признака {feature_name}: {feature_value}. Ошибка: {e}")
            
            # Создаем DataFrame
            features_df = pd.DataFrame([processed_features], columns=self.feature_names)
            
            # Выполняем предсказание
            prediction = self.model.predict(features_df)
            
            return float(prediction[0])
            
        except Exception as e:
            print(f"Ошибка при выполнении предсказания: {e}")
            raise e