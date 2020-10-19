import pytest
from botocore.stub import Stubber
from glacier_upload.libraries.glacier_library import GlacierLib


@pytest.fixture
def glacier_lib(boto3_stub, temp_json):
    with boto3_stub:
        glacier = GlacierLib('test_vault', upload_log=temp_json)
    return glacier
