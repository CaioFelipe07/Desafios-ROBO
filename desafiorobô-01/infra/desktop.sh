#!/usr/bin/env bash
set -euo pipefail
trap 'kill $(jobs -pr) 2>/dev/null || true' EXIT
Xvfb :1 -screen 0 1280x800x24 -ac +extension GLX +render -noreset &
for tentativa in $(seq 1 50); do
  if xdpyinfo -display :1 >/dev/null 2>&1; then break; fi
  sleep 0.2
done
xdpyinfo -display :1 >/dev/null
fluxbox >/tmp/fluxbox.log 2>&1 &
x11vnc -display :1 -localhost -forever -shared -nopw -rfbport 5900 >/tmp/vnc.log 2>&1 &
websockify --web /usr/share/novnc 6080 localhost:5900 &
wait -n
