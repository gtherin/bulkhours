#!/usr/bin/env bash
set -euo pipefail

cd /home/pi/bulkhours/bulkhours/bots/cars
exec python -m uvicorn web_server:app --host 0.0.0.0 --port 8000
