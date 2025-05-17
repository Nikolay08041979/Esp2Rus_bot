
# 📄 tools/rollback_analytics.py

"""
Скрипт отката: отключает стек аналитики v2 и возвращает проект к v1.
Поддерживает параметры:
    --config ../core/config.py
    --backup analytics_old/analytics_v1_backup.py
    --target analytics/analytics_v1_backup.py
"""

import os
from pathlib import Path
import argparse

def rollback_flag_in_config(config_path: str):
    path = Path(config_path)
    if not path.exists():
        print(f"[ERROR] config.py не найден по пути: {config_path}")
        return

    content = path.read_text()
    if "USE_ANALYTICS_V2 = True" in content:
        updated = content.replace("USE_ANALYTICS_V2 = True", "USE_ANALYTICS_V2 = False")
        path.write_text(updated)
        print("[OK] USE_ANALYTICS_V2 выключен в config.py")
    else:
        print("[INFO] Флаг уже выключен или строка не найдена.")

def restore_backup_file(backup_path: str, target_path: str):
    if Path(backup_path).exists():
        os.replace(backup_path, target_path)
        print("[OK] analytics_v1_backup.py восстановлен из резервной копии.")
    else:
        print(f"[WARN] Файл резервной копии не найден: {backup_path}")

def main():
    parser = argparse.ArgumentParser(description="Откат аналитического стека V2.")
    parser.add_argument("--config", default="../core/config.py", help="Путь до config.py")
    parser.add_argument("--backup", default="../analytics_old/analytics_v1_backup.py", help="Файл резервной копии analytics")
    parser.add_argument("--target", default="../analytics/analytics_v1_backup.py", help="Файл, который нужно восстановить")

    args = parser.parse_args()

    rollback_flag_in_config(args.config)
    restore_backup_file(args.backup, args.target)

if __name__ == "__main__":
    main()
