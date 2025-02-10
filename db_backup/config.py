"""Configuration module for database backup"""

import configparser
import os
import sys


def load_db_config(config_path="config.ini"):
    """Load database configuration from config file"""
    if not os.path.exists(config_path):
        print(f"Error: {config_path} file not found!")
        print("Please create a config file with your database credentials.")
        sys.exit(1)

    config = configparser.ConfigParser()
    config.read(config_path)
    return config["MySQL"]


def load_gdrive_config(config_path="config.ini"):
    """Load Google Drive configuration from config file"""
    if not os.path.exists(config_path):
        print(f"Error: {config_path} file not found!")
        print("Please create a config file with your Google Drive settings.")
        sys.exit(1)

    config = configparser.ConfigParser()
    config.read(config_path)

    # Return None if section doesn't exist
    if "GoogleDrive" not in config:
        return None

    # Convert section to dictionary
    return dict(config["GoogleDrive"])
