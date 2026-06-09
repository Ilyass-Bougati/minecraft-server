#!/usr/bin/env bash
set -e

# Keep the Space "Running" by answering HTTP on the proxied port
python3 /usr/local/bin/status.py &

# ngrok reads NGROK_AUTHTOKEN from env automatically; dials out over 443
if [ -n "${NGROK_AUTHTOKEN}" ]; then
  ngrok tcp 25565 --log=stdout > /tmp/ngrok.log 2>&1 &
else
  echo "WARNING: NGROK_AUTHTOKEN not set — server won't be reachable from outside."
fi

# Hand off to itzg's normal startup (downloads jar+mods over 443, runs MC in foreground)
exec /start
