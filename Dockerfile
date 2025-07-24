FROM python:3.11

WORKDIR /shopmate

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY api ./api

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
