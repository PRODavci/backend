#!/bin/sh
alembic upgrade head

cd app

sh -c "python main.py"
