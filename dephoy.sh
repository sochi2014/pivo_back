#!/bin/sh


echo "Running Alembic migrations..."
python -m alembic upgrade head

echo "DUMP"
sqlite3 database.db < database.sql

echo "Start docker-compose"
docker compose up -d --build
echo "Deployment completed successfully!"
