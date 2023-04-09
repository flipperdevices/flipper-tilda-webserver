#!/bin/sh

set -eu;

nginx &
gunicorn --bind 0.0.0.0:5000 app:app --timeout=90

wait -n
exit $?
