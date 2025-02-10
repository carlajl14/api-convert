#!/bin/bash
source myenv/bin/activate
exec gunicorn -w 4 -k uvicorn.workers.UvicornWorker api.main:app