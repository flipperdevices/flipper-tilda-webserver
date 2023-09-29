#!/bin/bash

set -euo pipefail

gunicorn --bind 0.0.0.0:5000 app:app --timeout=300 &
nginx &

wait -n
exit $?
