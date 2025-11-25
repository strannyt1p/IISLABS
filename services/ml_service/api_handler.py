import mlflow.pyfunc
import pandas as pd
import os
import numpy as np

class FastAPIHandler:
    def __init__(self, model_path: str = "/models/model"):
        """
        Инициализация обработчика - загрузка модели в формате MLflow
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
        Загрузка модели в формате MLflow
        """
        try:
            # Проверяем существование пути
            if not os.path.exists(self.model_path):
                raise FileNotFoundError(f"Путь к модели не существует: {self.model_path}")
            
            print(f"Загружаем модель из: {self.model_path}")
            model = mlflow.pyfunc.load_model(self.model_path)
            print("Модель успешно загружена")
            return model
        except Exception as e:
            print(f"Ошибка при загрузке модели: {e}")
            raise e
    
    def predict(self, features: list) -> float:
        """
        Выполнение предсказания на основе признаков
        """
        try:
            # Проверяем количество признаков
            if len(features) != len(self.feature_names):
                raise ValueError(f"Ожидается {len(self.feature_names)} признаков, получено {len(features)}")
            
            # Создаем словарь для данных с правильными типами
            data_dict = {}
            
            # Обрабатываем каждый признак отдельно
            for i, feature_name in enumerate(self.feature_names):
                value = features[i]
                
                # Для числовых признаков преобразуем к правильному типу
                if feature_name in ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 
                                   'thalach', 'exang', 'slope', 'ca', 'thal']:
                    data_dict[feature_name] = [int(value)]
                elif feature_name in ['oldpeak', 'chol_age_ratio']:
                    data_dict[feature_name] = [float(value)]
                else:  # строковые признаки
                    data_dict[feature_name] = [str(value)]
            
            # Создаем DataFrame
            features_df = pd.DataFrame(data_dict)
            
            # Явно задаем типы для числовых колонок
            int_columns = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 
                          'thalach', 'exang', 'slope', 'ca', 'thal']
            float_columns = ['oldpeak', 'chol_age_ratio']
            
            for col in int_columns:
                features_df[col] = features_df[col].astype('int64')
            for col in float_columns:
                features_df[col] = features_df[col].astype('float64')
            
            print(f"Типы данных в DataFrame:")
            print(features_df.dtypes)
            print(f"Данные для предсказания:")
            print(features_df)
            
            # Выполняем предсказание
            prediction = self.model.predict(features_df)
            
            print(f"Результат предсказания: {prediction}")
            
            # Возвращаем первое значение предсказания
            return float(prediction[0])
            
        except Exception as e:
            print(f"Ошибка при выполнении предсказания: {e}")
            raise e