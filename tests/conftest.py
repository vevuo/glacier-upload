import os
from random import randint
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
    ]
    content_large = [str(randint(0, 1)) for _ in range(0, 4294304)]
    content.append("".join(content_large))
    for i, _ in enumerate(range(0, len(content))):
        f = test_dir.join(f"file.txt.00{i}")
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
