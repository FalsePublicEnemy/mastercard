FROM python:3.9-alpine

WORKDIR /app

COPY . /app

RUN apk update

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

CMD ["sh", "runserver.sh"]

# Could add docker-compose for running test inside container
# f.e. docker-compose run --rm tests -vv -x /app/tests.py
# f.e. docker-compose run --rm lint
