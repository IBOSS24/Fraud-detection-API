FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN mkdir -p /app/logs

COPY api ./api
COPY models ./models

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]