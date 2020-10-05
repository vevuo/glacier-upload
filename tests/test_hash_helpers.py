from glacier_upload.libraries import hash_helpers as helpers


expected_hashes = [
    "957d77a7df3a9bf068f93204a373b556074a02d108cc8a5b8d617661014f4e40",
    "117de21a5c3f79389667af7212f91c24f33cc92fc8fb3dfce2eaf7dd4f624203",
    "8162e509861bf0b9ccdb512d6abb780ed03beacb777c62b761562a9c2458de5d",
]


def test_add_hashes(test_files):
    hashes_added = helpers.add_hashes(test_files)
    assert hashes_added[0].get("hash") == expected_hashes[0]
    assert hashes_added[1].get("hash") == expected_hashes[1]
    assert hashes_added[2].get("hash") == expected_hashes[2]


def test_get_hash(test_files):
    result_hash = helpers.get_hash(test_files[0])
    assert result_hash == expected_hashes[0]


def test_get_total_hash(test_files):
    hashes_added = helpers.add_hashes(test_files)
    result_total_hash = helpers.get_total_hash(hashes_added)
    assert result_total_hash == "2a6e851a9a2533e00c2532340de472c3b70b2f33d5a3521c5812903530c85aea"
