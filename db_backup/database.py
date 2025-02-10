"""Database backup module"""

import os
import subprocess
import datetime
from typing import Dict


def create_backup(config: Dict[str, str]) -> str:
    """Create database backup using mariadb-dump

    Args:
        config: Dictionary containing database configuration
               (host, user, password, database, port)

    Returns:
        str: Path to the created backup file

    Raises:
        Exception: If backup creation fails
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"backup_{config['database']}_{timestamp}.sql"

    # Construct mariadb-dump command
    dump_cmd = [
        "mariadb-dump",
        f"--host={config['host']}",
        f"--user={config['user']}",
        f"--password={config['password']}",
        f"--port={config['port']}",
        "--single-transaction",
        "--quick",
        "--compress",
        "--routines",
        "--triggers",
        "--events",
        "--ssl-verify-server-cert=false",
        config["database"],
        f"--result-file={backup_file}",
    ]

    try:
        # Execute mariadb-dump
        print(f"Creating backup of database '{config['database']}'...")
        process = subprocess.run(dump_cmd, capture_output=True, text=True)

        if process.returncode == 0:
            size_mb = os.path.getsize(backup_file) / (1024 * 1024)
            print(f"Backup successfully created: {backup_file}")
            print(f"Backup size: {size_mb:.2f} MB")
            return backup_file
        else:
            print("Error creating backup:")
            print(process.stderr)
            if os.path.exists(backup_file):
                os.remove(backup_file)
            raise Exception("Database backup failed")

    except Exception as e:
        if os.path.exists(backup_file):
            os.remove(backup_file)
        raise Exception(f"Database backup failed: {str(e)}")
