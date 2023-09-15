import sys
from pathlib import Path
import pytest

sys.path.insert(1, str(Path(__file__).parent.parent))

from src.pyCloudUpload.upload import Upload
from src.pyCloudUpload.exceptions import InvalidUploadDirectoryException


@pytest.fixture
def upload_object():
    return Upload(Path(__file__).parent / "sample_files")


def remove_path(result):
    return [filename for filename, file_path in result]


def test_upload_wrong_path_exception():
    with pytest.raises(InvalidUploadDirectoryException):
        Upload(Path(__file__).parent / "sample_files" / "level0_reciept.pdf")


def test_filter_media_files(upload_object: Upload):
    assert [
        "level0_movie.mp4",
        "level2_A_profile_verification.wmv",
        "level1_B_sun2_movie.3gp",
        "level1_B_kengan_ashura.mp3",
    ] == remove_path(upload_object.get_media())


def test_filter_document_files(upload_object: Upload):
    assert [
        "level0_docu_1.doc",
        "level0_reciept.pdf",
        "level1_A_data.csv",
        "level2_A_bill_pay.pdf",
        "level1_B_reciept.docx",
        "level2_B_ufc_contract.docx",
    ] == remove_path(upload_object.get_document())


def test_filter_image_files(upload_object: Upload):
    assert [
        "level0_samp.jpg",
        "level1_A_photo.png",
        "level3_A_icon.svg",
    ] == remove_path(upload_object.get_image())
