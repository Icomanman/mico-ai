
import os
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from dotenv import load_dotenv
import io
import json

load_dotenv()


class Drive:
    """
        Requires a Service account file and scopes url.
    """

    def __init__(self):
        with open('./tmp/json.env', 'r') as json_file:
            SERVICE_KEY = json.load(json_file)

        SCOPES = os.environ.get('SCOPES')

        credentials = service_account.Credentials.from_service_account_info(
            SERVICE_KEY, scopes=SCOPES)
        self.service = build('drive', 'v3', credentials=credentials)

        if not credentials.token:
            raise ValueError('> Credentials validations failed.')

    def download(self, file_id: str = ''):
        if not os.path.exists('./tmp'):
            os.mkdir('./tmp')

        local_path = './tmp'
        req = self.service.files().get_media(fileId=file_id)
        fh = io.FileIO(f'{local_path}/dsa.py', 'wb')  # binary
        downloader = MediaIoBaseDownload(fh, req)

        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))

        return

    def upload(self, file_path: str, folder_id: str):
        file_metadata = {
            'name': os.path.basename(file_path),
            'parents': [folder_id]
        }
        media_body = MediaFileUpload(file_path, resumable=True)
        file = self.service.files().create(
            body=file_metadata,
            media_body=media_body
        ).execute()
        print('File ID:', file['id'])

        return
