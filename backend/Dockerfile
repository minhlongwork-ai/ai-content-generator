FROM python:3.12-slim

WORKDIR /app

ENV PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
