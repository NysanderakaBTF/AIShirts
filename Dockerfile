FROM python:3.11-alpine

WORKDIR /var/www
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .
RUN apk update \
    && pip3 install --upgrade pip && pip3 install -r requirements.txt

COPY . .

CMD python3 manage.py makemigrations && python3 manage.py migrate