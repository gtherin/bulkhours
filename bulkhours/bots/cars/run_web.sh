#!/usr/bin/env bash
# /home/pi/bulkhours/bulkhours/bots/cars/run_web.sh
set -euo pipefail

source /home/pi/venvs/picarx/bin/activate
cd /home/pi/bulkhours/bulkhours/bots/cars

APP_PATTERNS=(
	"python -m uvicorn web_server:app"
	"python -X faulthandler -m uvicorn web_server:app"
	"uvicorn web_server:app"
)

stop_web_server_processes() {
	local sig="$1"
	local pattern
	for pattern in "${APP_PATTERNS[@]}"; do
		pkill "$sig" -f "$pattern" 2>/dev/null || true
	done
}

camera_holder_pids() {
	fuser /dev/video0 /dev/media0 /dev/media4 2>/dev/null | grep -Eo '[0-9]+' | sort -u || true
}

echo "Cleaning previous web/camera processes..."

# 1) Graceful stop first, then force-kill leftovers.
stop_web_server_processes ""
sleep 1
if pgrep -f "uvicorn web_server:app" >/dev/null 2>&1; then
	stop_web_server_processes "-9"
	sleep 1
fi

# 2) If camera is still held, kill only holders related to this app.
for pid in $(camera_holder_pids); do
	cmd="$(ps -p "$pid" -o args= 2>/dev/null || true)"
	if echo "$cmd" | grep -Eq 'uvicorn web_server:app|web_server.py|vilib'; then
		kill -9 "$pid" 2>/dev/null || true
	fi
done
sleep 1

# 3) Hard fail early if camera remains busy by unrelated processes.
holders="$(camera_holder_pids | tr '\n' ' ')"
if [[ -n "${holders// }" ]]; then
	echo "Camera devices are still busy (PIDs: $holders)"
	echo "Run: fuser -v /dev/video0 /dev/media0 /dev/media4"
	exit 1
fi

# Use pure-Python protocol/loop implementations for better stability on Raspberry Pi
# when Vilib (Flask + picamera2 stack) runs in the same process.
exec python -m uvicorn web_server:app --host 0.0.0.0 --port 8000 --loop asyncio --http h11 --ws websockets
