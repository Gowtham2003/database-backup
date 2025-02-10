#!/usr/bin/env python3

"""Cron script for automated database backups"""

import os
import sys
import logging
from datetime import datetime
from pathlib import Path
from db_backup.config import load_db_config, load_gdrive_config
from db_backup.database import create_backup
from db_backup.gdrive import upload_file


# Setup logging
def setup_logging():
    """Setup logging configuration"""
    # Create logs directory if it doesn't exist
    log_dir = Path(__file__).parent / "logs"
    log_dir.mkdir(exist_ok=True)

    # Setup logging
    log_file = log_dir / f'backup_{datetime.now().strftime("%Y%m")}.log'
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stdout)],
    )
    return logging.getLogger(__name__)


def cleanup_local_backup(backup_file: str, logger: logging.Logger):
    """Delete local backup file after successful upload

    Args:
        backup_file: Path to the backup file
        logger: Logger instance
    """
    try:
        if os.path.exists(backup_file):
            os.remove(backup_file)
            logger.info(f"Local backup file deleted: {backup_file}")
    except Exception as e:
        logger.warning(f"Failed to delete local backup file: {str(e)}")


def main():
    """Main backup function for cron job"""
    logger = setup_logging()
    backup_file = None

    try:
        # Get script directory
        script_dir = Path(__file__).parent.absolute()
        os.chdir(script_dir)  # Change to script directory

        logger.info("Starting database backup process")

        # Load configurations
        db_config = load_db_config()
        gdrive_config = load_gdrive_config()

        # Create backup
        logger.info("Creating database backup...")
        backup_file = create_backup(db_config)
        logger.info(f"Backup created successfully: {backup_file}")

        # Upload to Google Drive if configured
        if gdrive_config and gdrive_config.get("folder_id"):
            logger.info("Uploading backup to Google Drive...")
            file_id = upload_file(backup_file, folder_id=gdrive_config["folder_id"])
            logger.info(
                f"Backup uploaded successfully to Google Drive. File ID: {file_id}"
            )

            # Delete local backup file after successful upload
            cleanup_local_backup(backup_file, logger)

        logger.info("Backup process completed successfully")

    except Exception as e:
        logger.error(f"Backup failed: {str(e)}")
        # Clean up local backup file if it exists and there was an error
        if backup_file and os.path.exists(backup_file):
            cleanup_local_backup(backup_file, logger)
        sys.exit(1)


if __name__ == "__main__":
    main()
