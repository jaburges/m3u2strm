FROM python:3.9-slim

# Install required dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    cron \
    gettext-base \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy your Python application
COPY . .

# Install Python dependencies (assuming you have requirements.txt)
RUN pip install --no-cache-dir -r requirements.txt

# Create directory for STRM files
RUN mkdir -p /movieoutput
RUN mkdir -p /TVEpisodesoutput  

# Add crontab file
COPY crontab /etc/cron.d/m3u2strm
RUN chmod 0644 /etc/cron.d/m3u2strm

# Create the log file
RUN touch /var/log/cron.log

# Script to update environment variables in crontab and start services
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"] 