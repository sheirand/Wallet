#!/bin/sh

set -e

echo "Celery worker starting..."

sleep 10

# For stats queue
celery -A core worker -Q stats_queue -B -c 2 -l info --loglevel=INFO -n worker2@%n

exec "$@"
