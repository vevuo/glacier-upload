import os
import json
import pytest
from glacier_backup.libraries import response_storage


@pytest.fixture(scope="session")
def temp_json(tmpdir_factory):
    #temp_json_content = {
    #    "archives": []
    #}
    fn = tmpdir_factory.mktemp("test_data").join("uploaded.json")
    #with open(fn, "w") as temp_file:
    #    json.dump(temp_json_content, temp_file, indent=4)
    return fn


def test_storage_init(temp_json):
    """Testing that the json file is created if it doesn't exist."""
    expected_content = {
        "archives": []
    }
    storage = response_storage.Storage(temp_json)
    with open(temp_json) as temp_file:
        temp_json_content = json.load(temp_file)
    assert expected_content == temp_json_content


def test_storage_init_file_exists(tmp_path):
    """Testing that nothing changes in the file if it exists when the
    Storage is initialized.
    """
    expected_content = {
        "archives": []
    }
    temp_json_dir = tmp_path / "data"
    temp_json_dir.mkdir()
    temp_json_file = os.path.join(temp_json_dir, 'uploaded.json')
    with open(temp_json_file, "w") as temp_file:
        json.dump(expected_content, temp_file, indent=4)
    storage = response_storage.Storage(file_name=temp_json_file)
    with open(temp_json_file) as temp_file:
        temp_json_content = json.load(temp_file)
    assert expected_content == temp_json_content
 