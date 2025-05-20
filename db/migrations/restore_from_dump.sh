#!/bin/bash

# Используется вручную в случае аварийного восстановления

DB_NAME="esp2rus"
DUMP_FILE="backup_7_tables.sql"

# Создать БД, если её нет
if ! psql -U postgres -h localhost -lqt | cut -d \| -f 1 | grep -qw $DB_NAME; then
  echo "📦 Создаём базу данных $DB_NAME..."
  createdb -U postgres -h localhost $DB_NAME
fi

# Восстановление
echo "🔁 Восстанавливаем таблицы из $DUMP_FILE..."
psql -U postgres -h localhost -d $DB_NAME -f $DUMP_FILE
echo "✅ Готово."
