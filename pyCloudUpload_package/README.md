# `pyCloudUpload`

The pyCloudUpload is a Python package designed to simplify the process of reading and transferring files from a directory and its subdirectories to cloud storage services. This module supports various file types, including images (jpg, png, svg, and webp), media files (mp3, mp4, mpeg4, wmv, 3gp, and webm), and documents (doc, docx, csv, and pdf). You can configure this module to upload images and media files to AWS S3 and documents to Google Cloud Storage.

## Features

-   Read files of specific types (images, media, documents) from a directory and its subdirectories.
-   Upload images and media files to AWS S3.
-   Upload documents to Google Cloud Storage.
-   Configurable file type selection for S3 and Google Cloud.
-   A generic module that can be easily customized and utilized according to your needs.

## Installation

1. **Download the Wheel File**: First, obtain the Wheel file (.whl) for the package you want to install.

2. **Open a Terminal or Command Prompt**: Open a terminal or command prompt on your system with Python and pip installed.

3. **Navigate to the Directory Containing the Wheel File**:
    ```bash
    cd /path/to/directory
    ```
4. **Install the package**
    ```bash
    pip install pyCloudUpload_package-1.0.0-py3-none-any.whl
    ```
5. **Verification:** Import the package in Python to verify the installation:
    ```python
    pyCloudUpload.upload import Upload
    ```

## Usage

-   **Reading Files:** _You can use the following methods to retrieve files of specific types from a given directory and its subdirectories:_

```python
pyCloudUpload.upload import Upload

# create an object
upload = Upload("/path/to/directory")

# scan the directories for media
upload.get_media()
# or
upload.get_media(extensions=["png", "jpg", "svg"])

# scan the directories for images
upload.get_image()

# scan the directories for documents
upload.get_document()
```

-   **Uploading Files:** _To upload the files to AWS S3 and Google Cloud Storage, use the following methods:_

```python
pyCloudUpload.upload import Upload

"""Upload images and media files to AWS S3"""
upload.upload_to_aws(
    aws_secret_key="AWS_KEY",
    bucket="your bucket name",
    object_name="your object name",
    file_type = ["png", "svg"] # optional
)


"""Upload documents to Google Cloud Storage"""
# Google Cloud Storage Configuration
google_cloud_config = {
    'type': 'service_account',
    'client_id': os.environ['BACKUP_CLIENT_ID'],
    'client_email': os.environ['BACKUP_CLIENT_EMAIL'],
    'private_key_id': os.environ['BACKUP_PRIVATE_KEY_ID'],
    'private_key': os.environ['BACKUP_PRIVATE_KEY'],
}
upload.upload_to_gcp(
    credentials_dict= google_cloud_config,
    bucket="your bucket name",
    project="your project name",
    file_type = ["docx", "pdf"] # optional
)
```
