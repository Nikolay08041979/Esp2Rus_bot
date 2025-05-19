# Используем лёгкий Python-образ
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости (добавлен postgresql-client)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем Python-библиотеки
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Переменные среды
ENV PYTHONUNBUFFERED=1

# Запуск
CMD ["python", "main.py"]
