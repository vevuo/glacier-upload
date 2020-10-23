from glacier_upload.libraries import hash_helpers as helpers


expected_hash = "957d77a7df3a9bf068f93204a373b556074a02d108cc8a5b8d617661014f4e40"
expected_total_even_hash = "853af0ca4205181e58022b95e3dc6646a420500ad19ed089dc62030aa69e8f64"
expected_total_odd_hash = "9f025dae9287b6764cc6da2065ace65f31464ec70bb290fb0b46098dd857ee1c"


def test_get_tree_hash(test_files):
    result_tree_hash = helpers.get_tree_hash(test_files[0].get("file_path"))
    assert result_tree_hash == expected_hash


def test_get_part_hash():
    result_hash = helpers.get_part_hash(bytes("1000100111001111", encoding="utf-8"))
    assert result_hash == expected_hash


def test_get_total_hash_even_parts():
    static_parts = [
        bytes("1000100111001111", encoding="utf-8"),
        bytes("1000100111001111", encoding="utf-8"),
    ]
    part_hashes = []
    for part_data in static_parts:
        part_hashes.append(
            helpers.get_part_hash(part_data)
        )
    result_total_hash = helpers.get_total_hash(part_hashes)
    assert result_total_hash == expected_total_even_hash


def test_get_total_hash_odd_parts():
    static_parts = [
        bytes("1000100111001111", encoding="utf-8"),
        bytes("1000100111001111", encoding="utf-8"),
        bytes("1000100111", encoding="utf-8"),
    ]
    part_hashes = []
    for part_data in static_parts:
        part_hashes.append(
            helpers.get_part_hash(part_data)
        )
    result_total_hash = helpers.get_total_hash(part_hashes)
    assert result_total_hash == expected_total_odd_hash
