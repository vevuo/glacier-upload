import os
import sys
import json
import pytest
import boto3
from botocore.stub import Stubber
path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, path + '/../')
sys.path.insert(0, path + '/../glacier_backup/libraries')
from glacier_library import GlacierLib


@pytest.fixture(scope="session")
def temp_json(tmpdir_factory):
    fn = tmpdir_factory.mktemp("test_data").join("uploaded.json")
    return fn


@pytest.fixture(scope="session")
def single_test_file(tmpdir_factory):
    files = []
    fn = tmpdir_factory.mktemp("test_data").join("file.zip")
    files.append(str(os.path.abspath(fn)))
    with open(fn, "w") as file:
        file.write("test")
    return files


@pytest.fixture(scope="session")
def multiple_test_files(tmpdir_factory):
    files = []
    fn = tmpdir_factory.mktemp("test_data").join("file01.zip")
    fn2 = tmpdir_factory.mktemp("test_data").join("file02.zip")
    files.append(str(os.path.abspath(fn)))
    files.append(str(os.path.abspath(fn2)))
    with open(fn, "w") as file:
        file.write("test")
    with open(fn2, "w") as file:
        file.write("test2")
    return files


@pytest.fixture(scope="session")
def boto3_stub():
    client = boto3.client('s3')
    stubber = Stubber(client)
    return stubber


@pytest.fixture
def glacier_lib(boto3_stub, temp_json):
    with boto3_stub:
        glacier = GlacierLib('test_vault', storage_file=temp_json)
    return glacier


@pytest.fixture
def temp_storage_file(tmp_path):
    json_content = {
        "archives": []
    }
    temp_json = tmp_path / "uploaded.json"
    with open(temp_json, "w") as file:
        json.dump(json_content, file, indent=4)


def test__all_files_exist_single_file(single_test_file, glacier_lib):
    result = glacier_lib._check_if_all_files_exist(single_test_file)
    assert result


def test__all_files_exist_multiple_files(multiple_test_files, glacier_lib):
    result = glacier_lib._check_if_all_files_exist(multiple_test_files)
    assert result
