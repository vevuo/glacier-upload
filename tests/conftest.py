import os
import pytest
import boto3
from botocore.stub import Stubber
path = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture(scope="session")
def test_files(tmpdir_factory):
    test_dir = tmpdir_factory.mktemp("test_data")
    files = []
    content = [
        "1000100111001111",
        "1110101111001111",
        "100011",
    ]
    for i, _ in enumerate(range(1, 4)):
        f = test_dir.join(f"file{i}.zip.00{i}")
        f.write(content[i])
        files.append(
            {"file_path": str(os.path.abspath(f))}
        )
    return files


@pytest.fixture(scope="session")
def temp_json(tmpdir_factory):
    fn = tmpdir_factory.mktemp("test_data").join("uploaded.json")
    return fn


@pytest.fixture(scope="session")
def boto3_stub():
    client = boto3.client('s3')
    stubber = Stubber(client)
    return stubber
