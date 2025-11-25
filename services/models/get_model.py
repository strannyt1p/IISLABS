import mlflow
import os

def download_model(run_id: str, output_path: str = "../models"):
    """
    Загружает модель из MLflow по run_id и сохраняет в native формате MLflow
    """
    try:
        # Укажите URI для доступа к MLflow
        mlflow.set_tracking_uri("http://localhost:5000")
        
        print(f"Загружаем модель с run_id: {run_id}")
        
        # Скачиваем всю модель в директорию
        model_path = mlflow.artifacts.download_artifacts(
            run_id=run_id,
            artifact_path="model",
            dst_path=output_path
        )
        
        print(f"Модель успешно скачана в: {model_path}")
        print(f"Содержимое директории: {os.listdir(model_path)}")
        
        return model_path
        
    except Exception as e:
        print(f"Ошибка при загрузке модели: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    RUN_ID = "53cbd22b6ce74c6cb75023c10374863c"  # ваш run_id
    
    # Загружаем модель
    model_path = download_model(RUN_ID)
    
    if model_path:
        print("✅ Модель успешно загружена!")
    else:
        print("❌ Ошибка загрузки модели")