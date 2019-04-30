#! /usr/bin/env sh

./scripts/wait-for.sh postgres:5432 -- echo "postgres is up"
./scripts/wait-for.sh rabbitmq:5672 -- echo "rabbitmq is up"


export PYTHONPATH=src/services/
celery worker -A worker -Q photo-processor -c 1 &
python src/services/web.py
