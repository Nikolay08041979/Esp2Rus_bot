
# 📄 rollback_analytics.py

"""
Скрипт отката: отключает стек аналитики v2 и возвращает проект к v1 (если сохранена копия).
1. Меняет USE_ANALYTICS_V2 = False в .env или config
2. (Опционально) заменяет analytics.py на analytics_old/analytics_v1_backup.py
"""

import os
from pathlib import Path

ENV_FILE = ".env"
CONFIG_FILE = "core/config.py"
BACKUP_ANALYTICS = "analytics_old/analytics_v1_backup.py"
CURRENT_ANALYTICS = "analytics/analytics.py"

def rollback_flag_in_config():
    path = Path(CONFIG_FILE)
    if not path.exists():
        print(f"[ERROR] config.py не найден по пути: {CONFIG_FILE}")
        return

    content = path.read_text()
    if "USE_ANALYTICS_V2 = True" in content:
        updated = content.replace("USE_ANALYTICS_V2 = True", "USE_ANALYTICS_V2 = False")
        path.write_text(updated)
        print("[OK] USE_ANALYTICS_V2 выключен в config.py")
    else:
        print("[INFO] Флаг уже выключен.")

def restore_backup_file():
    if Path(BACKUP_ANALYTICS).exists():
        os.replace(BACKUP_ANALYTICS, CURRENT_ANALYTICS)
        print("[OK] analytics.py восстановлен из analytics_old/")
    else:
        print("[WARN] Файл резервной копии не найден.")

if __name__ == "__main__":
    rollback_flag_in_config()
    restore_backup_file()
