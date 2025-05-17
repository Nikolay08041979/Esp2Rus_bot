#!/bin/bash

# Папка проекта (замени путь на свой)
PROJECT_DIR="/home/kolya/Esp2Ru_bot"
LOG_DIR="$PROJECT_DIR/logs/cron"
SCRIPT_PATH="$PROJECT_DIR/db/migrations/update_client_levels.py"
PYTHON_BIN="/usr/bin/python3"  # или путь к venv, если используется

# Создаём директорию для логов, если не существует
mkdir -p "$LOG_DIR"

# Имя лог-файла с меткой даты
LOG_FILE="$LOG_DIR/level_update_$(date +%Y%m%d).log"

# Запуск скрипта и логирование
echo "[START] $(date)" >> "$LOG_FILE"
$PYTHON_BIN "$SCRIPT_PATH" >> "$LOG_FILE" 2>&1
echo "[END] $(date)" >> "$LOG_FILE"