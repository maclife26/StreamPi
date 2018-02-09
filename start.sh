#!/usr/bin/env bash

set -e

BASEDIR=$(dirname "$0")
LOGFILE="$BASEDIR/server.log"

echo "Comenzando en background y escribiendo log file $LOGFILE"
nohup python3 -u "$BASEDIR/main.py" "$@" &>> "$LOGFILE" &
