#!/bin/bash

echo "===== KAIRO SYSTEM STATUS DASHBOARD ====="

echo -e "\n[1] GitHub Sync (Last 3 Commits):"
cd ~/kairo && git pull > /dev/null
git log --oneline -n 3

echo -e "\n[2] Mid-Kairo Server Status (Port 4321):"
sudo lsof -i :4321 | grep LISTEN || echo "⚠️ Mid-Kairo not running!"

echo -e "\n[3] Cron Auto-Sync Status:"
crontab -l | grep kairo_sync.sh || echo "⚠️ Auto-sync not configured"

echo -e "\n[4] Last Auto-Sync Log Entry:"
tail -n 2 ~/kairo/sync_cron.log 2>/dev/null || echo "⚠️ No log found"

echo -e "\n[5] Laptop IP (use for Phone/Termux connection):"
hostname -I | awk '{print $1}'

echo -e "\n========================================="
echo "Run test from phone: curl -X POST http://<above-ip>:4321/ ..."



