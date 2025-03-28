#!/bin/bash
cd /home/girritharan/kairo
while true; do
    echo "$(date) - Kairo heartbeat" >> logs/kairo_daemon.log
    git pull origin main
    bash kairo_sync.sh
    sleep 900  # 15 minutes
done
