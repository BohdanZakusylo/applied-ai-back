FROM python:3.11-slim

WORKDIR /fastapi

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r ./requirements.txt

COPY ./app /fastapi/app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"] 