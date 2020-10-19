from glacier_upload.libraries import file_size_helpers as helpers


def test_get_file_size(test_files):
    file_size = helpers.get_file_size(test_files[1].get("file_path"))
    assert file_size == 4294304


def test_get_allowed_sizes():
    allowed_sizes = helpers.get_allowed_sizes()
    print(allowed_sizes)
    assert allowed_sizes.get("1") == 1048576
    assert allowed_sizes.get("2048") == 2147483648
    assert len(allowed_sizes) == 12


def test_get_needed_parts(test_files):
    expected_parts = [
        {"part_size": 1048576},
        {"part_size": 1048576},
        {"part_size": 1048576},
        {"part_size": 1048576},
        {"part_size": 100000},
    ]
    parts = helpers.get_needed_parts(
        test_files[1].get("file_path"),
        1048576,
        4294304
        )
    assert expected_parts == parts


def test_add_range_string():
    parts = [
        {"part_size": 1048576},
        {"part_size": 1048576},
        {"part_size": 100850},
    ]
    ranges_added = helpers.add_byte_ranges(parts)
    assert ranges_added[0].get("range") == "bytes 0-1048575/*"
    assert ranges_added[1].get("range") == "bytes 1048576-2097151/*"
    assert ranges_added[2].get("range") == "bytes 2097152-2198001/*"
