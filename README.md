# Bonjour Bichon 📸

Automatically send random photos from your Nextcloud to a Signal group. Features duplicate sending prevention within a configurable time period and automatic image resizing for optimal mobile viewing.

## Prerequisites

- **Docker** and **Docker Compose** installed
- **Nextcloud** instance with photos stored in a specific folder
- **Signal account** registered with the signal-cli-rest-api service

## Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/sylvaingable/bonjour-bichon
cd bonjour-bichon
cp .env.sample .env
```

### 2. Configure Environment

Edit `.env` with your settings:

```env
# How many days of history to keep (affects duplicate detection)
HISTORY_DAYS_COUNT=90

# How many pictures to send each time
PICTURES_PER_DAY_COUNT=3

# Message to send with the pictures
PICTURES_MESSAGE="Here are some photos! 📸"

# Nextcloud connection details
NEXTCLOUD_WEBDAV_URL=https://your-nextcloud.com/remote.php/dav
NEXTCLOUD_USERNAME=your-username
NEXTCLOUD_PASSWORD=your-password
NEXTCLOUD_PHOTOS_PATH=/files/your-username/Photos/

# Signal settings (using signal-cli-rest-api)
SIGNAL_BASE_URL=http://signal-cli-rest-api:8080
SIGNAL_SENDER=+1234567890
SIGNAL_GROUP_RECIPIENT='Family group"

# File to track sent pictures (update docker compose file accordingly if you need to change it)
SENT_PICTURES_PATH=./sent_pictures.txt
```

### 3. Setup Signal

The project uses [signal-cli-rest-api](https://github.com/bbernhard/signal-cli-rest-api) to send messages. You need to [link it to your phone number](https://github.com/bbernhard/signal-cli-rest-api?tab=readme-ov-file#getting-started).

**First time setup:**
```bash
# Start the Signal API service
docker-compose up -d signal-cli-rest-api

# Follow the signal-cli-rest-api documentation to register and link your phone number
# This typically involves QR code linking or SMS verification
```

### 4. Build and Test

```bash
# Build the application
docker-compose build bonjour-bichon

# Test run (make sure Signal API is running first)
docker-compose up -d signal-cli-rest-api
docker-compose run --rm bonjour-bichon
```

### Automated with Cron

Add to your crontab to run daily at 9 AM:

```bash
# Edit crontab
crontab -e

# Add this line (adjust path to your project directory)
0 9 * * * cd /path/to/bonjour-bichon && ocker-compose run --rm bonjour-bichon
```

### Automated with Systemd

Create a systemd service and timer:

**`/etc/systemd/system/bonjour-bichon.service`:**
```ini
[Unit]
Description=Send random photos via Signal
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
WorkingDirectory=/path/to/bonjour-bichon
ExecStart=/usr/bin/docker-compose run --rm bonjour-bichon
User=your-user
Group=your-group

[Install]
WantedBy=multi-user.target
```

**`/etc/systemd/system/bonjour-bichon.timer`:**
```ini
[Unit]
Description=Run bonjour-bichon daily
Requires=bonjour-bichon.service

[Timer]
OnCalendar=*-*-* 09:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

Enable and start:
```bash
sudo systemctl enable bonjour-bichon.timer
sudo systemctl start bonjour-bichon.timer
```
