#!/bin/sh

cd  /app
python init_server.py
gunicorn app:app --bind 0.0.0.0:8000 --worker-class sanic.worker.GunicornWorker -w 3

