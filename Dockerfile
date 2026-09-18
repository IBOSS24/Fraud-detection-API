FROM python:3.11

WORKDIR /app

ARG API_VERSION=0.0.0-dev
ENV API_VERSION=${API_VERSION}

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY api ./api
COPY models ./models

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]