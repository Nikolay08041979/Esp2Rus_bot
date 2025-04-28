import os
from datetime import datetime
import json

UPLOADS_DIR = "data/uploads"
LOGS_DIR = "data/logs"

# Инициализация папок
os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

def save_uploaded_csv(file_name: str, file_data: bytes) -> str:
    """Сохраняем загруженный CSV-файл в папку uploads/"""
    path = os.path.join(UPLOADS_DIR, file_name)
    with open(path, "wb") as f:
        f.write(file_data)
    return path

def save_import_log(result: dict) -> str:
    """Сохраняем лог результатов импорта"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join(LOGS_DIR, f"import_log_{timestamp}.json")
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    return log_path
