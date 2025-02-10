# Database Backup Tool

Automatically backup MySQL/MariaDB databases to Google Drive.

## Quick Start

1. Install required packages:

```bash
# Debian/Ubuntu
sudo apt install mariadb-client python3-venv

# RHEL/CentOS
sudo yum install MariaDB-client python3
```

2. Set up Google Drive:

   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create a project and enable Google Drive API
   - Create OAuth credentials (Desktop app)
   - Download and save as `credentials.json` in project folder

3. Configure:

```bash
# Copy and edit config file
cp config.ini.example config.ini
nano config.ini  # Add your database and Google Drive details
```

4. Run:

```bash
# Test backup manually
python3 backup_cron.py

# Or set up automated daily backups
./setup_cron.sh
```

## Logs

Check `logs/` directory for backup logs.
