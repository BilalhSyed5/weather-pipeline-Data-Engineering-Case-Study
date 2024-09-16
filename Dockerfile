FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY queries.py .

RUN mypy --strict main.py queries.py

CMD ["sh", "-c", "python main.py && python queries.py"]