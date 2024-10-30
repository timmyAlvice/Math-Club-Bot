# Используем базовый образ Ubuntu
FROM ubuntu:latest

# Установка необходимых пакетов
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-setuptools \
    python3-venv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Создаем директорию приложения
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .
COPY .env .

# Создаем виртуальное окружение
RUN python3 -m venv venv

# Активируем виртуальное окружение и устанавливаем зависимости
RUN . venv/bin/activate && pip install --no-cache-dir -r requirements.txt

# Копируем код приложения в контейнер
COPY . .

# Указываем команду для запуска при старте контейнера
CMD ["venv/bin/python", "main.py"]