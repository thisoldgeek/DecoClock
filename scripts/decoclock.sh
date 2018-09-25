#!/bin/sh
cd /home/pi/DecoClock/scripts
sudo cat decoclock_service.txt > /etc/systemd/system/decoclock.service
sudo chmod 644 /etc/systemd/system/decoclock.service
sudo systemctl daemon-reload
sudo systemctl enable decoclock
