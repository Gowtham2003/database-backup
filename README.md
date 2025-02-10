# MariaDB Database Backup Script

This Python script creates SQL dumps of MariaDB databases using `mariadb-dump` and stores them in the current directory.

## Prerequisites

- Python 3.6 or higher
- MariaDB client tools (`mariadb-dump`)
- Network access to the database server

## Setup

1. Make sure mariadb-dump is installed:

   ```bash
   # On Debian/Ubuntu
   sudo apt-get install mariadb-client

   # On RHEL/CentOS
   sudo yum install MariaDB-client
   ```

2. Copy `config.ini` and edit it with your database credentials:

   ```ini
   [MySQL]
   host = your_database_host
   user = your_username
   password = your_password
   database = your_database_name
   ```

3. Make the script executable:
   ```bash
   chmod +x backup_mysql.py
   ```

## Usage

Simply run the script:

```bash
./backup_mysql.py
```

The script will:

1. Connect to the specified database server
2. Create a SQL dump file named `backup_DATABASE_YYYYMMDD_HHMMSS.sql`
3. Display the backup file name and size upon completion

## Features

- Creates complete SQL dumps including:
  - Table structures and data
  - Stored procedures and functions
  - Triggers
  - Events
- Uses compression for efficient transfer from remote servers
- Timestamp-based backup file names
- Error handling and cleanup
- Progress feedback during backup

## Backup Options Included

The script uses these mariadb-dump options:

- `--single-transaction`: Consistent backup of InnoDB tables
- `--quick`: Better performance for large databases
- `--compress`: Compress data transfer between client and server
- `--routines`: Include stored procedures and functions
- `--triggers`: Include triggers
- `--events`: Include events

## Error Handling

The script will exit with an error message if:

- The `config.ini` file is missing
- Database credentials are incorrect
- Connection to database fails
- Backup process encounters an error

## Security Note

Keep your `config.ini` file secure as it contains database credentials. Consider:

- Setting restricted file permissions (600)
- Not committing it to version control
- Using environment variables for sensitive data in production

## Restoring the Backup

To restore the backup, you can use the mariadb command:

```bash
mariadb -h hostname -u username -p database_name < backup_file.sql
```
