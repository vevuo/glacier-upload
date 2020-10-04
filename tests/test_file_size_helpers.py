import os
import sys
import pytest
path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, path + '/../glacier_upload/libraries')
from file_size_helpers import *


def test_get_total_size(test_files):
    total_size = get_total_size(test_files)
    assert total_size == 38


def test_get_file_size(test_files):
    file_size = get_file_size(test_files[1].get("file_path"))
    assert file_size == 16


def test_add_file_size(test_files):
    size_added = add_file_size(test_files)
    assert size_added[0].get("file_size") == 16
    assert size_added[1].get("file_size") == 16
    assert size_added[2].get("file_size") == 6


def test_add_ranges(test_files):
    test_files_with_size = add_file_size(test_files)
    ranges_added = add_ranges(test_files_with_size)
    assert ranges_added[0].get("range") == "bytes 0-15/*"
    assert ranges_added[1].get("range") == "bytes 16-31/*"
    assert ranges_added[2].get("range") == "bytes 32-37/*"
