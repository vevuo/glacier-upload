import os
import sys
import pytest
import boto3
from botocore.stub import Stubber
path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, path + '/../')
sys.path.insert(0, path + '/../glacier_backup/libraries')
from glacier_library import GlacierLib


@pytest.fixture(scope="session")
def single_test_file(tmpdir_factory):
    files = []
    fn = tmpdir_factory.mktemp("test_data").join("file.zip")
    files.append(str(os.path.abspath(fn)))
    with open(fn, "w") as file:
        file.write("test")
    return files


@pytest.fixture
def boto3_stub():
    client = boto3.client('s3')
    stubber = Stubber(client)
    return stubber


@pytest.fixture
def glacier_lib(boto3_stub):
    with boto3_stub:
        glacier = GlacierLib('test_vault')
    return glacier


def test__all_files_exist(single_test_file, glacier_lib):
    result = glacier_lib._check_if_all_files_exist(single_test_file)
    assert result
