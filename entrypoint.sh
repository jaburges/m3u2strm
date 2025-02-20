#!/bin/bash

# Replace environment variables in crontab
envsubst < /etc/cron.d/m3u2strm > /etc/cron.d/m3u2strm.tmp
mv /etc/cron.d/m3u2strm.tmp /etc/cron.d/m3u2strm

# Start cron
cron

# Create required directories with proper permissions
mkdir -p /movieoutput/movies
mkdir -p /TVEpisodesoutput/tvshows
chmod -R 777 /movieoutput
chmod -R 777 /TVEpisodesoutput

# Run initial conversion
python /app/main.py

# Keep container running and follow cron logs
tail -f /var/log/cron.log 