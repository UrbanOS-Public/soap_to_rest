#!/usr/bin/env bash
service nginx start
gunicorn \
        --user $(id -u www-data) \
        --group $(id -g www-data) \
        --umask "0022" \
        --workers 1 \
        --bind unix:/tmp/uvicorn.sock \
        --error-logfile - \
        -k uvicorn.workers.UvicornWorker \
        soap_to_rest:app