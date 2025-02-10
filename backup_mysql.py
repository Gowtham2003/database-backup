#!/usr/bin/env python3

"""Main script for database backup with Google Drive upload"""

import sys
from db_backup.config import load_db_config, load_gdrive_config
from db_backup.database import create_backup
from db_backup.gdrive import upload_file


def main():
    try:
        # Load configurations
        db_config = load_db_config()
        gdrive_config = load_gdrive_config()

        # Create database backup
        backup_file = create_backup(db_config)

        # Upload to Google Drive if configured
        if gdrive_config and gdrive_config.get("folder_id"):
            upload_file(backup_file, folder_id=gdrive_config["folder_id"])

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
