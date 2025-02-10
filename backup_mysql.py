#!/usr/bin/env python3

import os
import subprocess
import datetime
import configparser
import sys


def load_config():
    """Load database configuration from config.ini file"""
    if not os.path.exists("config.ini"):
        print("Error: config.ini file not found!")
        print("Please create a config.ini file with your database credentials.")
        sys.exit(1)

    config = configparser.ConfigParser()
    config.read("config.ini")
    return config["MySQL"]


def create_backup(host, user, password, database, port):
    """Create database backup using mariadb-dump"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"backup_{database}_{timestamp}.sql"

    # Construct mariadb-dump command
    dump_cmd = [
        "mariadb-dump",  # Use mariadb-dump instead of mysqldump
        f"--host={host}",
        f"--user={user}",
        f"--password={password}",
        f"--port={port}",
        "--single-transaction",  # For consistent backup of InnoDB tables
        "--quick",  # Faster for large databases
        "--compress",  # Compress data between client and server
        "--routines",  # Include stored procedures and functions
        "--triggers",  # Include triggers
        "--events",  # Include events
        "--ssl-verify-server-cert=false",  # Disable SSL certificate verification
        database,
        f"--result-file={backup_file}",
    ]

    try:
        # Execute mariadb-dump
        print(f"Creating backup of database '{database}'...")
        process = subprocess.run(dump_cmd, capture_output=True, text=True)

        if process.returncode == 0:
            size_mb = os.path.getsize(backup_file) / (1024 * 1024)
            print(f"Backup successfully created: {backup_file}")
            print(f"Backup size: {size_mb:.2f} MB")
        else:
            print("Error creating backup:")
            print(process.stderr)
            if os.path.exists(backup_file):
                os.remove(backup_file)
            sys.exit(1)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        if os.path.exists(backup_file):
            os.remove(backup_file)
        sys.exit(1)


def main():
    try:
        # Load configuration
        config = load_config()

        # Get database configuration
        host = config.get("host", "localhost")
        user = config.get("user")
        password = config.get("password")
        database = config.get("database")
        port = config.get("port")

        # Create backup
        create_backup(host, user, password, database, port)

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
