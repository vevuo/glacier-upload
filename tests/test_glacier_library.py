import pytest
from botocore.stub import Stubber
from glacier_upload.libraries.glacier_library import GlacierLib


@pytest.fixture
def glacier_lib(boto3_stub, temp_json):
    with boto3_stub:
        glacier = GlacierLib('test_vault', storage_file=temp_json)
    return glacier


def test__all_files_exist_single_file(test_files, glacier_lib):
    result = glacier_lib._check_if_all_files_exist([test_files[0]])
    assert result


def test__all_files_exist_multiple_files(test_files, glacier_lib):
    result = glacier_lib._check_if_all_files_exist(test_files)
    assert result
