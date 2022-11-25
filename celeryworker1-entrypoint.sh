#!/bin/sh

set -e

echo "Celery worker starting..."

sleep 10

# For email queue
celery -A core worker -Q mailing_queue -c 2 -l info --loglevel=INFO -n worker1@%n

exec "$@"
