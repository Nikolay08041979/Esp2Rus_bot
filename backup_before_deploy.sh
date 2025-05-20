#!/bin/bash
# backup_before_deploy.sh

set -e

### ✅ Загрузка переменных из .env
export $(grep -v '^#' .env | xargs)

### 🔐 Переменные БД (берутся из .env)
DB_NAME="${DB_NAME:-esp2rus}"
DB_USER="${DB_USER:-postgres}"
DB_HOST="${DB_HOST:-db}"        # по умолчанию — имя docker-сервиса
DB_PASSWORD="${DB_PASSWORD:-secret}"
BACKUP_FILE="backup_7_tables_$(date +%Y-%m-%d_%H-%M).sql"

### 📦 Список таблиц
TABLES=(
  client_info
  client_analytics
  dictionary
  word_category
  study_level
  study_levels
  learned_words
)

echo "🔄 Делаем бэкап перед деплоем..."

PGPASSWORD=$DB_PASSWORD pg_dump -U "$DB_USER" -h "$DB_HOST" -d "$DB_NAME" \
  $(for table in "${TABLES[@]}"; do echo -n "-t $table "; done) \
  > "$BACKUP_FILE"

echo "✅ Бэкап успешно создан: $BACKUP_FILE"

# ✅ Копируем в стандартный файл для восстановления
cp "$BACKUP_FILE" backup_7_tables.sql
echo "📌 Также скопировано в backup_7_tables.sql для run_install.py"