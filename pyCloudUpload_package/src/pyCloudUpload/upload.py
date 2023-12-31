from pathlib import Path
from .exceptions import InvalidUploadDirectoryException

# AWS & GCP imports
from google.cloud import storage as gcp_storage
import boto3
from botocore.exceptions import ClientError


class Upload:
    def __init__(self, directory: str | Path) -> None:
        self.directory = Path(directory) if isinstance(directory, str) else directory
        if not self.directory.exists() or not self.directory.is_dir():
            raise InvalidUploadDirectoryException

    def __get_files_filtered_with_extensions(self, extensions: list) -> list[tuple]:
        """Scans through the directories and sub-directories to get all the files with given extension(s)

        Args:
            extensions (list): List of extenions to filter the files from

        Returns:
            list[tuple]: List of tuple(filename, file_path)
        """
        files = []
        # iterate recursively through the directories
        for item in self.directory.rglob("*"):
            # ignore dirs and filter extenions
            if item.is_file() and item.suffix[1:] in extensions:
                files.append((item.name, str(item.resolve())))

        return files

    def get_image(self, extensions: list = ["jpg", "png", "svg", "webp"]) -> list[tuple]:
        """Scans through the directories and sub-directories to get all the files associated with images

        Args:
            extensions (list, optional): List fo extensions. Defaults to ["jpg", "png", "svg", "webp"].

        Returns:
            list: List of tuple(filename, file_path)
        """

        return self.__get_files_filtered_with_extensions(extensions)

    def get_media(
        self, extensions: list = ["mp3", "mp4", "mpeg4", "wmv", "3gp", "webm"]
    ) -> list[tuple]:
        """Scans through the directories and sub-directories to get all the files associated with media

        Args:
            extensions (list, optional): _description_. Defaults to ["mp3", "mp4", "mpeg4", "wmv", "3gp", "webm"].

        Returns:
            list: _description_
        """
        return self.__get_files_filtered_with_extensions(extensions)

    def get_document(self, extensions: list = ["doc", "docx", "csv", "pdf"]) -> list[tuple]:
        """Scans through the directories and sub-directories to get all the files associated with documents

        Args:
            extensions (list, optional): _description_. Defaults to ["doc", "docx", "csv", "pdf"].

        Returns:
            list: _description_
        """

        return self.__get_files_filtered_with_extensions(extensions)

    def upload_to_aws(
        self,
        bucket,
        object_name: str = None,
        file_type: list | tuple = [],
        args=None,
    ) -> bool:
        """Upload to AWS, core code for AWS upload from -> https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html

        Args:
            bucket (_type_): Bucket Name
            object_name (str, optional): Object name. Defaults to None.
            file_type_extenion (list | tuple, optional): File extensions, this will upload all the files found in the directory. Defaults to [].
            files (list[Path  |  str], optional): List of file paths to upload. Defaults to [].
            args: Additional arguments to S3 client

        Returns:
            bool: True if file was uploaded, else False
        """

        s3_client = boto3.client("s3")
        files_to_upload = None

        if file_type:  # for extesions given by the user to upload all the files
            files_to_upload = self.__get_files_filtered_with_extensions(file_type)
        else:
            files_to_upload = self.get_image() + self.get_media()

        for filename, file_path in files_to_upload:
            # set object name if None
            if object_name is None:
                object_name = filename
            # Upload the file
            try:
                response = s3_client.upload_file(
                    str(file_path), bucket, object_name, ExtraArgs=args
                )
            except ClientError as e:
                return False
        return True

    def upload_to_gcp(
        self,
        bucket_name: str,
        credentials_file: str,
        file_type: list | tuple = [],
    ) -> bool:
        """Upload to Google Cloud, core code for GCP upload from -> https://www.educative.io/answers/how-to-upload-a-file-to-google-cloud-storage-on-python-3

        Args:
            bucket_name (str): Bucket Name
            credentials_file (str): GCP credentials json file path
            file_type (list | tuple, optional): List of file paths to upload. Defaults to [].

        Returns:
            bool: True if file was uploaded, else False
        """

        # Initialize the Google Cloud Storage client with the credentials
        storage_client = gcp_storage.Client.from_service_account_json(credentials_file)
        # Get the target bucket
        bucket = storage_client.bucket(bucket_name)

        if file_type:  # for extesions given by the user to upload all the files
            files_to_upload = self.__get_files_filtered_with_extensions(file_type)
        else:
            files_to_upload = self.get_document()

        for filename, file_path in files_to_upload:
            try:
                # Upload the file to the bucket
                blob = bucket.blob(filename)
                blob.upload_from_filename(file_path)
            except Exception:
                return False

        return True
