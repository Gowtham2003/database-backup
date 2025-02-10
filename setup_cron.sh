#!/bin/bash

# Make scripts executable
chmod +x backup_cron.py
chmod +x backup_mysql.py

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
source venv/bin/activate
pip install -r requirements.txt

# Get absolute path of the backup script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKUP_SCRIPT="$SCRIPT_DIR/backup_cron.py"
PYTHON_PATH="$SCRIPT_DIR/venv/bin/python"

# Create cron job
echo "Setting up cron job..."
(crontab -l 2>/dev/null; echo "0 3 * * * cd $SCRIPT_DIR && $PYTHON_PATH $BACKUP_SCRIPT >> $SCRIPT_DIR/logs/cron.log 2>&1") | crontab -

echo "Cron job has been set up to run daily at 3 AM"
echo "You can edit the schedule using 'crontab -e'"
echo "Logs will be available in the logs directory"

# Set secure permissions for config file
chmod 600 config.ini 