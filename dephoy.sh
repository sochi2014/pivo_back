#!/bin/sh

echo "Updating packages and installing sqlite3..."
sudo apt-get update && sudo apt-get install -y sqlite3

echo "Running Alembic migrations..."
python -m alembic upgrade head

echo "Start docker-compose"
docker compose up -d --build
echo "Deployment completed successfully!"
