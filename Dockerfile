FROM python:3.10-alpine
WORKDIR /code

COPY Pipfile .
COPY Pipfile.lock .
COPY api.py .
COPY .env .

RUN pip install pipenv

RUN pipenv install --system --deploy --ignore-pipfile



