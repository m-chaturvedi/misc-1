#!/usr/bin/env bash
set -euo pipefail
function cleanup {
    echo "Sending SIGKILL to $PID"
    kill -9 $PID
}

trap cleanup EXIT

rm -f canvass.db
python3 server.py &
PID=$!
sleep 3
python3 -m pytest --pdb -s
python3 simulator.py
