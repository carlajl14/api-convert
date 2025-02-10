#!/bin/bash
source /home/carlapython/api-convert/myenv/bin/activate
exec gunicorn -w 4 -k uvicorn.workers.UvicornWorker api.main:app