"""Google Drive backup module"""

import os
from typing import Dict, Optional
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Use the most restrictive scope possible
SCOPES = [
    "https://www.googleapis.com/auth/drive.file"
]  # Only access to files created by the app


def get_gdrive_service():
    """Get Google Drive API service instance"""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("drive", "v3", credentials=creds)


def create_backup_folder(service, folder_name: str = "Database Backups") -> str:
    """Create a dedicated folder for backups if it doesn't exist

    Args:
        service: Google Drive service instance
        folder_name: Name of the backup folder

    Returns:
        str: ID of the backup folder
    """
    # Check if folder already exists
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    results = (
        service.files().list(q=query, spaces="drive", fields="files(id)").execute()
    )
    folders = results.get("files", [])

    if folders:
        return folders[0]["id"]

    # Create new folder
    folder_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
    }
    folder = service.files().create(body=folder_metadata, fields="id").execute()
    return folder.get("id")


def upload_file(
    file_path: str, folder_id: Optional[str] = None, config: Optional[Dict] = None
) -> str:
    """Upload file to Google Drive

    Args:
        file_path: Path to the file to upload
        folder_id: Optional Google Drive folder ID to upload to
        config: Optional configuration dictionary

    Returns:
        str: ID of the uploaded file
    """
    try:
        service = get_gdrive_service()

        # Create or get backup folder if folder_id not provided
        if not folder_id:
            folder_id = create_backup_folder(service)

        # Prepare file metadata
        file_metadata = {"name": os.path.basename(file_path), "parents": [folder_id]}

        # Upload file
        media = MediaFileUpload(file_path, mimetype="application/sql", resumable=True)

        print(f"Uploading {file_path} to Google Drive backup folder...")
        file = (
            service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )

        print(f"File uploaded successfully. File ID: {file.get('id')}")
        return file.get("id")

    except Exception as e:
        raise Exception(f"Failed to upload to Google Drive: {str(e)}")
