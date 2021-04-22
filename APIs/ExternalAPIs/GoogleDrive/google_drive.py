from __future__ import annotations
import os
from googleapiclient.http import MediaFileUpload
from APIs.ExternalAPIs import TalpiotSettings
from APIs.ExternalAPIs.WorkerPool.pool import Pool
from APIs.ExternalAPIs.WorkerPool.pooled_worker import PooledWorker

#  If modifying this scopes, delete token.json
SCOPES_DRIVE = ['https://www.googleapis.com/auth/drive']
MAX_WORKERS = 5


class GoogleDrive(PooledWorker):
    """
    A class that allows accessing GoogleDrive with
    the bot google account.
    """
    _pool = Pool(lambda: GoogleDrive(), MAX_WORKERS)

    @staticmethod
    def get_instance() -> GoogleDrive:
        return GoogleDrive._pool.get_free_worker()

    def __init__(self):
        super().__init__()
        self.creds_diary = None
        self.service = None

        self.connect_to_drive()

    def connect_to_drive(self):
        token_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "token.pickle"
        )

        google_settings = TalpiotSettings.get().google_connection_settings
        self.service = google_settings.get_service('drive', 'v3', SCOPES_DRIVE, token_file_path=token_path)

    def get_files_details(self):
        """
        Returns an result dictionary that has details about the specific
        spreadsheet.

        :param spreadsheet_id: The ID of the GoogleDrive document
        :return: dict
        """

        result = self.service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)"
        ).execute()

        return result

    def get_files(self, folder_id='', file_name='', advanced_query='', no_folders=False, only_folders=False, only_media=False):
        """
        Returns files in the folder_id given, according to the filters.
        :param folder_id: The folder id to search in
        :param file_name: Specific filename to return
        :param advanced_query: Option to add specific rules of your own (see Google Drive's API)
        :param no_folders: Do not list folders
        :param only_folders: List only folders
        :param only_media: List only media (images/videos)
        :return:
        """
        q: str = advanced_query
        if folder_id != '':
            q += ' ' + ('and ' if len(q) > 0 else '') + "'" + folder_id + "'" + ' in parents'
        if file_name != '':
            q += ' ' + ('and ' if len(q) > 0 else '') + "name = '" + file_name + "'"
        if no_folders:
            q += ' ' + ('and ' if len(q) > 0 else '') + "mimeType != 'application/vnd.google-apps.folder'"
        elif only_folders:
            q += ' ' + ('and ' if len(q) > 0 else '') + "mimeType = 'application/vnd.google-apps.folder'"
        if only_media:
            q += ' ' + ('and ' if len(q) > 0 else '') + "mimeType contains 'image/' or mimeType contains 'video/'"
        result = self.service.files().list(
            pageSize=100, fields="nextPageToken, files(id, name, mimeType, parents, )"
        ).execute()

        return result.get('files', [])

    def upload_image(self, image_path: str, image_name: str, folder_id: str = ''):
        """
        Returns an result dictionary that has details about the specific
        spreadsheet.

        :param folder_id: (optional) the id of the folder to upload to.
                          can be typed manualy or found through "get_files".
        :param image_path: local path of image to upload
        :param image_name: name for the cated image on the drive
        :return: str: the id of the created file in the drive
        """

        file_metadata = {'name': image_name}
        if folder_id != '':
            file_metadata['parents'] = [folder_id]
        media = MediaFileUpload(image_path,
                                mimetype='image/jpeg')
        file = self.service .files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()
        print('File ID: %s' % file.get('id'))
        return file.get('id')

    def upload_file(self, file_path: str, file_name: str, folder_id: str = ''):
        """
        Returns an result dictionary that has details about the specific
        spreadsheet.

        :param folder_id: (optional) the id of the folder to upload to.
                          can be typed manualy or found through "get_files".
        :param file_path: local path of file to upload
        :param file_name: name for the cated file on the drive
        :return: str: the id of the created file in the drive
        """

        file_metadata = {'name': file_name}
        if folder_id != '':
            print(folder_id)
            file_metadata['parents'] = [folder_id]
        media = MediaFileUpload(file_path,
                                resumable=True)
        file = self.service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()


if __name__ == "__main__":
    TalpiotSettings()
    with GoogleDrive.get_instance() as gd:
        pass