FROM python:3.10-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt update $$ apt install -y python-3-venv python-pip postgresql
RUN mkdir /www && \
    mkdir /www/src && \
    mkdir /www/src/app \
WORKDIR /www/src/app
COPY ./requirements.txt ./
RUN pip install ---upgrade pip && \
    pip install --no-cache-dir -r requirements.txt \
    pip install gunicorn
COPY . .
RUN python manage.py collectstatic --noinput
#CMD ["gunicorn", "-w", "4", "--bind", ":8000", "weather.wsgi:application"]
