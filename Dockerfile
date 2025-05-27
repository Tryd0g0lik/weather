FROM python:3
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt update &&
    apt install -y python3-venv python-pip postgresql-client
RUN mkdir /www && \
    mkdir /www/src && \
    mkdir /www/src/weather && \
    mkdir /www/src/weather/project && \
    mkdir /www/src/weather/templates && \
WORKDIR /www/src/weather
COPY ./requirements.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install gunicorn
COPY . .
RUN python manage.py collectstatic --noinput
#CMD ["gunicorn", "-w", "4", "--bind", ":8000", "weather.wsgi:application"]
