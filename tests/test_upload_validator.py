import pytest
from glacier_upload.libraries import upload_validator


@pytest.fixture
def validator():
    return upload_validator.Validator()


def test__check_if_file_exist(validator, test_files):
    found = validator._check_if_file_exist(test_files[0].get("file_path"))
    assert found


def test__check_if_file_exist_no_file(validator):
    found = validator._check_if_file_exist("no_file.txt")
    assert not found


def test__check_if_valid_part_size_for_glacier_16mb(validator):
    result = validator._check_if_valid_part_size_for_glacier(16)
    assert result


def test__check_if_valid_part_size_for_glacier_2048mb(validator):
    result = validator._check_if_valid_part_size_for_glacier(2048)
    assert result


def test__check_if_valid_part_size_for_glacier_invalid(validator):
    result = validator._check_if_valid_part_size_for_glacier(12)
    assert not result
