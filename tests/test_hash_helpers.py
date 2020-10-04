import os
import sys
import pytest
path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, path + '/../glacier_upload/libraries')
from hash_helpers import *


def test_add_hashes(test_files):
    hashes_added = add_hashes(test_files)
    assert hashes_added[0].get("hash") == "957d77a7df3a9bf068f93204a373b556074a02d108cc8a5b8d617661014f4e40"
    assert hashes_added[1].get("hash") == "117de21a5c3f79389667af7212f91c24f33cc92fc8fb3dfce2eaf7dd4f624203"
    assert hashes_added[2].get("hash") == "8162e509861bf0b9ccdb512d6abb780ed03beacb777c62b761562a9c2458de5d"


def test_get_hash(test_files):
    result_hash = get_hash(test_files[0])
    assert result_hash == "957d77a7df3a9bf068f93204a373b556074a02d108cc8a5b8d617661014f4e40"


def test_get_total_hash(test_files):
    hashes_added = add_hashes(test_files)
    result_total_hash = get_total_hash(hashes_added)
    assert result_total_hash == "cec30bde1c63d2d9169f3bba1aa136077864844de69b83c2c2c2d985979ea012"
