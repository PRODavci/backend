#!/bin/sh
alembic upgrade head

cd app

sh -c "python main.py --workers ${APP_WORKERS} --env ${APP_ENV}"
