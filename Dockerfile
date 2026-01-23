# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.14

# Установка системных зависимостей (для psycopg2, cron и т.д.)
RUN apt-get update && apt-get install -y \
    # cron \
    nano \
    lsof \
    tzdata \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Set timezone to Europe/Moscow
ENV TZ=Europe/Moscow


# Копируем requirements и устанавливаем venv
COPY app/requirements.txt .
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"
RUN python -m pip install -r requirements.txt
RUN python -m pip install "fastapi[all]"

# Копируем весь код проекта
COPY . .

# Настройка cron: предполагаем, что у тебя есть crontab файл (betmy.crontab) и скрипт collect_data.py
# RUN mkdir /etc/cron.d/api
# COPY app/environment/api.crontab /etc/cron.d/api
# RUN ls -la /etc/cron.d/*
# RUN chmod 0644 /etc/cron.d/api
# RUN crontab /etc/cron.d/api/api.crontab
# RUN touch /var/log/cron.log

# Инсталлируем все пакеты под VEnv для Bash-скрипта
WORKDIR /app
RUN bash -c "source /venv/bin/activate"
RUN python -m pip install -r requirements.txt
RUN python -m pip install "fastapi[all]"
# RUN deactivate


# RUN cron

EXPOSE 4000

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
#RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
#USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# File wsgi.py was not found. Please enter the Python path to wsgi file.
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "pythonPath.to.wsgi"]
# CMD python manage.py runserver 0.0.0.0:8000
CMD ["fastapi", "dev", "app.main:app", "--port", "4000", "--host", "0.0.0.0"]

