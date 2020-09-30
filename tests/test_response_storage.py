import os
import json
import pytest
from glacier_upload.libraries import response_storage


@pytest.fixture
def storage(temp_json):
    return response_storage.Storage(file_name=temp_json)


def test_storage_init(temp_json, storage):
    """Testing that the json file is created if it doesn't exist."""
    expected_content = {
        "archives": []
    }
    with open(temp_json) as temp_file:
        temp_json_content = json.load(temp_file)
    assert expected_content == temp_json_content


def test_storage_init_file_exists(temp_json):
    """Testing that nothing changes in the file if it exists when the
    Storage is initialized.
    """
    expected_content = {
        "archives": []
    }
    with open(temp_json, "w") as temp_file:
        json.dump(expected_content, temp_file, indent=4)
    storage = response_storage.Storage(file_name=temp_json)
    with open(temp_json) as temp_file:
        temp_json_content = json.load(temp_file)
    assert expected_content == temp_json_content


def test_save(temp_json, storage):
    expected_content = {
        "archives": [
            {
                "item": 1
            },
            {
                "item": "something",
                "list": [
                    'one',
                    'two'
                ]
            }
        ]
    }
    storage.save({"item": 1})
    storage.save({
        "item": "something",
        "list": ['one', 'two']
        })
    with open(temp_json) as temp_file:
        temp_json_content = json.load(temp_file)
    assert expected_content == temp_json_content
