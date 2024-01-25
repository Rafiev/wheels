# Используем базовый образ Python
FROM python:3.8

# Устанавливаем переменные окружения для работы с Django
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию в /app
WORKDIR /app

# Копируем зависимости в контейнер
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Копируем проект в контейнер
COPY . /app/

# Выполняем миграции и создаем суперпользователя
RUN python manage.py migrate && \
    echo "from django.contrib.auth import get_user_model; \
          User = get_user_model(); \
          User.objects.create_superuser('admin@example.com', 'adminpass')" | python manage.py shell

# Команда для запуска сервера
CMD python manage.py runserver 0.0.0.0:8000