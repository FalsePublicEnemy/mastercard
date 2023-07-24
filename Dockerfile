FROM python:3.9-alpine

WORKDIR /app

COPY . /app

RUN apk update

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

CMD ["sh", "runserver.sh"]