FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install "fastapi[standard]"

RUN apt-get update && apt-get install -y sqlite3

RUN python -m alembic upgrade head

RUN sqlite3 /app/database.db < /app/database.sql

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
