#!/usr/bin/env bash
service nginx start
cd /app/server
uwsgi --ini uwsgi.ini
