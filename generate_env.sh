#!/bin/bash
# generate_env.sh — создаёт .env в формате с комментариями

cat <<EOF > .env
# === Telegram Bot ===
BOT_TOKEN_PROD=${BOT_TOKEN_PROD:-your_real_prod_token}               # токен боевого бота

# === PostgreSQL ===
DB_USER=postgres
DB_PASSWORD=${DB_PASSWORD:-your_secure_password}
DB_NAME_PROD=esp2rus                                # основная база
DB_NAME=esp2rus                                     # основная база
DB_HOST=db                                          # ⚠️ Docker: "db", локально: "localhost"
DB_PORT=5432

# === Admins ===
ADMIN_IDS=${ADMIN_IDS:-admin_TG_id1,admin_TG_id2,admin_TG_id3}

# === Flags ===
ENV_MODE=prod                                      # dev | prod
DEBUG=0                                               # 1 = localhost / 0 = Docker

# === Персонализация / аналитика (дефолты) ===
USE_ANALYTICS_V2=True                      # новый аналитический стек
EOF

echo "✅ .env файл создан со всеми параметрами."
