#!/bin/bash

set -euo pipefail

gunicorn --bind 0.0.0.0:5000 app:app --timeout=90 &
nginx &

wait -n
exit $?
