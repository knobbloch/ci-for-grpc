FROM python:3.11-slim

WORKDIR /app

COPY . ./

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app/generated:/app/src:/app/db:/app

CMD ["python", "src/kitchen_server.py"]