FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# 🔽 Добавляем wait-for-it
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

COPY ./backend /app

# ❗ Меняем CMD на вызов через wait-for-it
CMD ["/wait-for-it.sh", "db:5432", "--", "daphne", "-b", "0.0.0.0", "-p", "8000", "backend.asgi:application"]