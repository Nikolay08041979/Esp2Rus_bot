#!/bin/bash

# Папка проекта
PROJECT_DIR="/root/Esp2Rus_bot"
LOG_DIR="$PROJECT_DIR/logs/cron"
SCRIPT_PATH="$PROJECT_DIR/analytics/metrics/run_sync_all_clients_with_tg_notify.py"
PYTHON_BIN="/usr/bin/python3"  # или путь до venv/bin/python

# Проверка, существует ли скрипт
if [ ! -f "$SCRIPT_PATH" ]; then
  echo "[ERROR] Script not found: $SCRIPT_PATH"
  exit 1
fi

# Создаём лог-папку, если не существует
mkdir -p "$LOG_DIR"

# Имя лог-файла
LOG_FILE="$LOG_DIR/level_update_$(date +%Y%m%d).log"

# Логируем запуск
{
  echo "=============================="
  echo "[START] $(date)"
  $PYTHON_BIN "$SCRIPT_PATH"
  echo "[END] $(date)"
  echo "=============================="
} >> "$LOG_FILE" 2>&1
